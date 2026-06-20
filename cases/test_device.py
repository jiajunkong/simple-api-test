import json
import uuid
import sqlite3
import pytest
from api.device_api import DeviceAPI
from db.db_init import init_db, clean_db

DB_PATH = "test.db"

with open("data/test_data.json", encoding="utf-8") as f:
    TEST_DATA = json.load(f)


def generate_device_id(prefix):
    return prefix + "_" + str(uuid.uuid4())[:8]


@pytest.fixture(autouse=True)
def setup_db():
    init_db(DB_PATH)
    clean_db(DB_PATH)
    yield
    clean_db(DB_PATH)


@pytest.fixture
def api():
    return DeviceAPI()


class TestDevice:
    def test_register_device_success(self, api):
        data = TEST_DATA["valid_device"]
        device_id = generate_device_id(data["device_id"])

        res = api.register_device(device_id, data["device_name"], data["device_type"])

        assert res.status_code == 200
        assert res.json()["code"] == 200
        assert res.json()["message"] == "设备注册成功"

    def test_register_device_duplicate(self, api):
        data = TEST_DATA["duplicate_device"]
        device_id = generate_device_id(data["device_id"])

        api.register_device(device_id, data["device_name"], data["device_type"])
        res = api.register_device(device_id, data["device_name"], data["device_type"])

        assert res.status_code == 400
        assert res.json()["message"] == "设备已存在"

    def test_login_device_success(self, api):
        data = TEST_DATA["valid_device"]
        device_id = generate_device_id(data["device_id"])

        api.register_device(device_id, data["device_name"], data["device_type"])
        res = api.login_device(device_id)

        assert res.status_code == 200
        assert "token" in res.json()

    def test_report_status_success(self, api):
        data = TEST_DATA["valid_device"]
        device_id = generate_device_id(data["device_id"])

        api.register_device(device_id, data["device_name"], data["device_type"])
        api.login_device(device_id)
        res = api.report_status(device_id, "online")

        assert res.status_code == 200
        assert res.json()["message"] == "状态上报成功"

    def test_report_status_without_token(self, api):
        data = TEST_DATA["valid_device"]
        device_id = generate_device_id(data["device_id"])

        api.register_device(device_id, data["device_name"], data["device_type"])
        res = api.report_status(device_id, "online")

        assert res.status_code == 401
        assert res.json()["message"] == "未登录，请先登录"

    def test_report_data_success(self, api):
        data = TEST_DATA["valid_device"]
        sensor = TEST_DATA["sensor_data"]
        device_id = generate_device_id(data["device_id"])

        api.register_device(device_id, data["device_name"], data["device_type"])
        api.login_device(device_id)
        res = api.report_data(
            device_id,
            sensor["temperature"],
            sensor["humidity"],
            sensor["battery"]
        )

        assert res.status_code == 200
        assert res.json()["message"] == "数据上报成功"

    def test_report_data_with_alert(self, api):
        data = TEST_DATA["valid_device"]
        alert = TEST_DATA["alert_data"]
        device_id = generate_device_id(data["device_id"])

        api.register_device(device_id, data["device_name"], data["device_type"])
        api.login_device(device_id)
        res = api.report_data(
            device_id,
            alert["temperature"],
            alert["humidity"],
            alert["battery"]
        )

        assert res.status_code == 200
        assert "温度超限" in res.json()["data"]["alerts"]
        assert "电量过低" in res.json()["data"]["alerts"]

    def test_get_device_success(self, api):
        data = TEST_DATA["valid_device"]
        device_id = generate_device_id(data["device_id"])

        api.register_device(device_id, data["device_name"], data["device_type"])
        api.login_device(device_id)
        res = api.get_device(device_id)

        assert res.status_code == 200
        assert res.json()["data"]["device_id"] == device_id


class TestDeviceDatabase:
    def test_register_device_db_check(self, api):
        data = TEST_DATA["valid_device"]
        device_id = generate_device_id(data["device_id"])

        res = api.register_device(device_id, data["device_name"], data["device_type"])

        assert res.status_code == 200

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT device_id, device_name FROM devices WHERE device_id = ?",
            (device_id,)
        )
        device = cursor.fetchone()
        conn.close()

        assert device is not None
        assert device[0] == device_id
        assert device[1] == data["device_name"]

    def test_report_data_db_check(self, api):
        data = TEST_DATA["valid_device"]
        sensor = TEST_DATA["sensor_data"]
        device_id = generate_device_id(data["device_id"])

        api.register_device(device_id, data["device_name"], data["device_type"])
        api.login_device(device_id)
        api.report_data(
            device_id,
            sensor["temperature"],
            sensor["humidity"],
            sensor["battery"]
        )

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT temperature, humidity, battery FROM sensor_data WHERE device_id = ?",
            (device_id,)
        )
        record = cursor.fetchone()
        conn.close()

        assert record is not None
        assert record[0] == sensor["temperature"]
        assert record[1] == sensor["humidity"]
        assert record[2] == sensor["battery"]

    def test_alert_db_check(self, api):
        data = TEST_DATA["valid_device"]
        alert = TEST_DATA["alert_data"]
        device_id = generate_device_id(data["device_id"])

        api.register_device(device_id, data["device_name"], data["device_type"])
        api.login_device(device_id)
        api.report_data(
            device_id,
            alert["temperature"],
            alert["humidity"],
            alert["battery"]
        )

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT alert_type, alert_value FROM alerts WHERE device_id = ?",
            (device_id,)
        )
        alerts = cursor.fetchall()
        conn.close()

        assert len(alerts) == 2
        alert_types = [a[0] for a in alerts]
        assert "temperature_high" in alert_types
        assert "battery_low" in alert_types