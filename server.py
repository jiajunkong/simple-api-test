from flask import Flask, request, jsonify, g
from db.db_init import get_connection, init_db

app = Flask(__name__)

# 存储token
tokens = {}


def get_db():
    """获取当前请求的数据库连接"""
    if 'db' not in g:
        g.db = get_connection("test.db")
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """请求结束后关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def check_token():
    """校验token，成功返回用户名，失败返回None"""
    token = request.headers.get("Authorization")
    if not token:
        return None
    return tokens.get(token)


# ========== 用户接口（保留）==========

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "code": 400,
            "message": "用户名和密码不能为空"
        }), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return jsonify({
            "code": 400,
            "message": "用户已存在"
        }), 400

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    db.commit()

    return jsonify({
        "code": 200,
        "message": "注册成功",
        "data": {
            "user_id": cursor.lastrowid
        }
    }), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()

    if not user:
        return jsonify({
            "code": 404,
            "message": "用户不存在"
        }), 404

    if user["password"] != password:
        return jsonify({
            "code": 401,
            "message": "密码错误"
        }), 401

    token = "token-" + username
    tokens[token] = username

    return jsonify({
        "code": 200,
        "message": "登录成功",
        "token": token
    }), 200


@app.route("/users/<username>", methods=["GET"])
def get_user(username):
    current_user = check_token()
    if not current_user:
        return jsonify({
            "code": 401,
            "message": "未登录，请先登录"
        }), 401

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, username, created_at FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()

    if not user:
        return jsonify({
            "code": 404,
            "message": "用户不存在"
        }), 404

    return jsonify({
        "code": 200,
        "message": "查询成功",
        "data": {
            "id": user["id"],
            "username": user["username"],
            "created_at": user["created_at"]
        }
    }), 200


@app.route("/profile", methods=["GET"])
def get_profile():
    current_user = check_token()
    if not current_user:
        return jsonify({
            "code": 401,
            "message": "未登录，请先登录"
        }), 401

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, username, created_at FROM users WHERE username = ?",
        (current_user,)
    )
    user = cursor.fetchone()

    return jsonify({
        "code": 200,
        "message": "查询成功",
        "data": {
            "id": user["id"],
            "username": user["username"],
            "created_at": user["created_at"]
        }
    }), 200


# ========== 设备接口（新增）==========

@app.route("/devices/register", methods=["POST"])
def register_device():
    data = request.get_json()
    device_id = data.get("device_id")
    device_name = data.get("device_name")
    device_type = data.get("device_type", "sensor")

    if not device_id or not device_name:
        return jsonify({
            "code": 400,
            "message": "设备ID和设备名称不能为空"
        }), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id FROM devices WHERE device_id = ?", (device_id,))
    if cursor.fetchone():
        return jsonify({
            "code": 400,
            "message": "设备已存在"
        }), 400

    cursor.execute(
        "INSERT INTO devices (device_id, device_name, device_type) VALUES (?, ?, ?)",
        (device_id, device_name, device_type)
    )
    db.commit()

    return jsonify({
        "code": 200,
        "message": "设备注册成功",
        "data": {
            "device_id": device_id
        }
    }), 200


@app.route("/devices/login", methods=["POST"])
def login_device():
    data = request.get_json()
    device_id = data.get("device_id")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, device_id, device_name FROM devices WHERE device_id = ?",
        (device_id,)
    )
    device = cursor.fetchone()

    if not device:
        return jsonify({
            "code": 404,
            "message": "设备不存在"
        }), 404

    token = "device-token-" + device_id
    tokens[token] = device_id

    return jsonify({
        "code": 200,
        "message": "设备登录成功",
        "token": token
    }), 200


@app.route("/devices/status", methods=["POST"])
def report_status():
    data = request.get_json()
    device_id = data.get("device_id")
    status = data.get("status")

    current_device = check_token()
    if not current_device:
        return jsonify({
            "code": 401,
            "message": "未登录，请先登录"
        }), 401

    if current_device != device_id:
        return jsonify({
            "code": 403,
            "message": "无权操作其他设备"
        }), 403

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE devices SET status = ? WHERE device_id = ?",
        (status, device_id)
    )
    db.commit()

    return jsonify({
        "code": 200,
        "message": "状态上报成功",
        "data": {
            "device_id": device_id,
            "status": status
        }
    }), 200


@app.route("/devices/data", methods=["POST"])
def report_data():
    data = request.get_json()
    device_id = data.get("device_id")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    battery = data.get("battery")

    current_device = check_token()
    if not current_device:
        return jsonify({
            "code": 401,
            "message": "未登录，请先登录"
        }), 401

    if current_device != device_id:
        return jsonify({
            "code": 403,
            "message": "无权操作其他设备"
        }), 403

    db = get_db()
    cursor = db.cursor()

    # 插入传感器数据
    cursor.execute(
        "INSERT INTO sensor_data (device_id, temperature, humidity, battery) VALUES (?, ?, ?, ?)",
        (device_id, temperature, humidity, battery)
    )

    # 检查告警
    alerts = []
    if temperature and temperature > 50:
        cursor.execute(
            "INSERT INTO alerts (device_id, alert_type, alert_value) VALUES (?, ?, ?)",
            (device_id, "temperature_high", str(temperature))
        )
        alerts.append("温度超限")

    if battery and battery < 20:
        cursor.execute(
            "INSERT INTO alerts (device_id, alert_type, alert_value) VALUES (?, ?, ?)",
            (device_id, "battery_low", str(battery))
        )
        alerts.append("电量过低")

    db.commit()

    return jsonify({
        "code": 200,
        "message": "数据上报成功",
        "data": {
            "device_id": device_id,
            "alerts": alerts
        }
    }), 200


@app.route("/devices/<device_id>", methods=["GET"])
def get_device(device_id):
    current_device = check_token()
    if not current_device:
        return jsonify({
            "code": 401,
            "message": "未登录，请先登录"
        }), 401

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, device_id, device_name, device_type, status, created_at FROM devices WHERE device_id = ?",
        (device_id,)
    )
    device = cursor.fetchone()

    if not device:
        return jsonify({
            "code": 404,
            "message": "设备不存在"
        }), 404

    return jsonify({
        "code": 200,
        "message": "查询成功",
        "data": {
            "id": device["id"],
            "device_id": device["device_id"],
            "device_name": device["device_name"],
            "device_type": device["device_type"],
            "status": device["status"],
            "created_at": device["created_at"]
        }
    }), 200


@app.route("/devices/<device_id>/alerts", methods=["GET"])
def get_device_alerts(device_id):
    current_device = check_token()
    if not current_device:
        return jsonify({
            "code": 401,
            "message": "未登录，请先登录"
        }), 401

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, alert_type, alert_value, status, created_at FROM alerts WHERE device_id = ? ORDER BY created_at DESC",
        (device_id,)
    )
    alerts = cursor.fetchall()

    return jsonify({
        "code": 200,
        "message": "查询成功",
        "data": {
            "device_id": device_id,
            "alerts": [
                {
                    "id": alert["id"],
                    "alert_type": alert["alert_type"],
                    "alert_value": alert["alert_value"],
                    "status": alert["status"],
                    "created_at": alert["created_at"]
                }
                for alert in alerts
            ]
        }
    }), 200


if __name__ == "__main__":
    init_db("test.db")
    app.run(debug=True, port=5000)