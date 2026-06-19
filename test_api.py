import requests

BASE_URL = "http://127.0.0.1:5000"


def test_register_success():
    """测试正常注册"""
    res = requests.post(BASE_URL + "/register", json={
        "username": "user001",
        "password": "123456"
    })

    assert res.status_code == 200
    assert res.json()["code"] == 200
    assert res.json()["message"] == "注册成功"


def test_register_duplicate():
    """测试重复注册"""
    # 先注册一次
    requests.post(BASE_URL + "/register", json={
        "username": "user002",
        "password": "123456"
    })

    # 再注册同样的用户名
    res = requests.post(BASE_URL + "/register", json={
        "username": "user002",
        "password": "123456"
    })

    assert res.status_code == 400
    assert res.json()["message"] == "用户已存在"


def test_login_success():
    """测试正常登录"""
    # 先注册
    requests.post(BASE_URL + "/register", json={
        "username": "user003",
        "password": "123456"
    })

    # 再登录
    res = requests.post(BASE_URL + "/login", json={
        "username": "user003",
        "password": "123456"
    })

    assert res.status_code == 200
    assert "token" in res.json()


def test_login_wrong_password():
    """测试密码错误"""
    # 先注册
    requests.post(BASE_URL + "/register", json={
        "username": "user004",
        "password": "123456"
    })

    # 用错误密码登录
    res = requests.post(BASE_URL + "/login", json={
        "username": "user004",
        "password": "wrongpassword"
    })

    assert res.status_code == 401
    assert res.json()["message"] == "密码错误"


def test_get_user_success():
    """测试查询存在的用户"""
    # 先注册
    requests.post(BASE_URL + "/register", json={
        "username": "user005",
        "password": "123456"
    })

    # 查询用户
    res = requests.get(BASE_URL + "/users/user005")

    assert res.status_code == 200
    assert res.json()["data"]["username"] == "user005"


def test_get_user_not_exist():
    """测试查询不存在的用户"""
    res = requests.get(BASE_URL + "/users/not_exist_user")

    assert res.status_code == 404
    assert res.json()["message"] == "用户不存在"