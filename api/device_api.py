from config.config import BASE_URL
from utils.request_util import RequestUtil


class DeviceAPI:
    def __init__(self):
        self.request = RequestUtil(BASE_URL)
        self.token = None

    def register_device(self, device_id, device_name, device_type="sensor"):
        return self.request.post(
            "/devices/register",
            json={
                "device_id": device_id,
                "device_name": device_name,
                "device_type": device_type
            }
        )

    def login_device(self, device_id):
        res = self.request.post(
            "/devices/login",
            json={
                "device_id": device_id
            }
        )
        if res.status_code == 200:
            self.token = res.json().get("token")
        return res

    def report_status(self, device_id, status):
        headers = {}
        if self.token:
            headers["Authorization"] = self.token

        return self.request.post(
            "/devices/status",
            json={
                "device_id": device_id,
                "status": status
            },
            headers=headers
        )

    def report_data(self, device_id, temperature, humidity, battery):
        headers = {}
        if self.token:
            headers["Authorization"] = self.token

        return self.request.post(
            "/devices/data",
            json={
                "device_id": device_id,
                "temperature": temperature,
                "humidity": humidity,
                "battery": battery
            },
            headers=headers
        )

    def get_device(self, device_id):
        headers = {}
        if self.token:
            headers["Authorization"] = self.token

        return self.request.get(
            f"/devices/{device_id}",
            headers=headers
        )

    def get_alerts(self, device_id):
        headers = {}
        if self.token:
            headers["Authorization"] = self.token

        return self.request.get(
            f"/devices/{device_id}/alerts",
            headers=headers
        )