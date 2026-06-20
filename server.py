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

    # 检查用户是否已存在
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return jsonify({
            "code": 400,
            "message": "用户已存在"
        }), 400

    # 插入用户
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

    # 查询用户
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

    # 生成token
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


if __name__ == "__main__":
    init_db("test.db")
    app.run(debug=True, port=5000)