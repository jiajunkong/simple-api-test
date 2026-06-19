import json
import uuid
import pytest
from api.user_api import UserAPI


# 加载测试数据
with open("data/test_data.json", encoding="utf-8") as f:
    TEST_DATA = json.load(f)


def generate_username(prefix):
    """生成唯一用户名，避免重复注册"""
    return prefix + "_" + str(uuid.uuid4())[:8]


@pytest.fixture
def api():
    return UserAPI()


class TestUser:
    def test_register_success(self, api):
        """测试注册成功"""
        data = TEST_DATA["valid_user"]
        username = generate_username(data["username"])

        res = api.register(username, data["password"])

        assert res.status_code == 200
        assert res.json()["code"] == 200
        assert res.json()["message"] == "注册成功"

    def test_register_duplicate(self, api):
        """测试重复注册"""
        data = TEST_DATA["duplicate_user"]
        username = generate_username(data["username"])

        api.register(username, data["password"])
        res = api.register(username, data["password"])

        assert res.status_code == 400
        assert res.json()["message"] == "用户已存在"

    def test_login_success(self, api):
        """测试登录成功"""
        data = TEST_DATA["valid_user"]
        username = generate_username(data["username"])

        api.register(username, data["password"])
        res = api.login(username, data["password"])

        assert res.status_code == 200
        assert "token" in res.json()

    def test_login_wrong_password(self, api):
        """测试密码错误"""
        data = TEST_DATA["wrong_password_user"]
        username = generate_username(data["username"])

        api.register(username, data["password"])
        res = api.login(username, data["wrong_password"])

        assert res.status_code == 401
        assert res.json()["message"] == "密码错误"

    def test_get_user_success(self, api):
        """测试登录后查询用户成功"""
        data = TEST_DATA["valid_user"]
        username = generate_username(data["username"])

        api.register(username, data["password"])
        api.login(username, data["password"])
        res = api.get_user(username)

        assert res.status_code == 200
        assert res.json()["data"]["username"] == username

    def test_get_user_not_exist(self, api):
        """测试登录后查询不存在的用户"""
        data = TEST_DATA["valid_user"]
        username = generate_username(data["username"])

        api.register(username, data["password"])
        api.login(username, data["password"])
        res = api.get_user("not_exist_user_xxx")

        assert res.status_code == 404
        assert res.json()["message"] == "用户不存在"

    def test_get_user_without_token(self, api):
        """测试不带token查询用户"""
        data = TEST_DATA["valid_user"]
        username = generate_username(data["username"])

        api.register(username, data["password"])
        res = api.get_user(username)

        assert res.status_code == 401
        assert res.json()["message"] == "未登录，请先登录"

    def test_get_profile_success(self, api):
        """测试带token获取当前用户信息"""
        data = TEST_DATA["valid_user"]
        username = generate_username(data["username"])

        api.register(username, data["password"])
        api.login(username, data["password"])
        res = api.get_profile()

        assert res.status_code == 200
        assert res.json()["data"]["username"] == username