from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟数据库
users = {}

# 模拟token存储
tokens = {}


def check_token():
    """校验token，校验成功返回用户名，失败返回None"""
    token = request.headers.get("Authorization")
    if not token:
        return None
    return tokens.get(token)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # 参数校验
    if not username or not password:
        return jsonify({
            "code": 400,
            "message": "用户名和密码不能为空"
        }), 400

    # 重复注册校验
    if username in users:
        return jsonify({
            "code": 400,
            "message": "用户已存在"
        }), 400

    # 保存用户
    users[username] = {
        "username": username,
        "password": password
    }

    return jsonify({
        "code": 200,
        "message": "注册成功"
    }), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # 用户不存在
    if username not in users:
        return jsonify({
            "code": 404,
            "message": "用户不存在"
        }), 404

    # 密码错误
    if users[username]["password"] != password:
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
    # 校验token
    current_user = check_token()
    if not current_user:
        return jsonify({
            "code": 401,
            "message": "未登录，请先登录"
        }), 401

    # 查询用户
    if username not in users:
        return jsonify({
            "code": 404,
            "message": "用户不存在"
        }), 404

    return jsonify({
        "code": 200,
        "message": "查询成功",
        "data": {
            "username": username
        }
    }), 200


@app.route("/profile", methods=["GET"])
def get_profile():
    """获取当前登录用户信息"""
    current_user = check_token()

    if not current_user:
        return jsonify({
            "code": 401,
            "message": "未登录，请先登录"
        }), 401

    return jsonify({
        "code": 200,
        "message": "查询成功",
        "data": {
            "username": current_user
        }
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)