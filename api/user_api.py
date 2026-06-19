from config.config import BASE_URL
from utils.request_util import RequestUtil


class UserAPI:
    def __init__(self):
        self.request = RequestUtil(BASE_URL)
        self.token = None

    def register(self, username, password):
        return self.request.post(
            "/register",
            json={
                "username": username,
                "password": password
            }
        )

    def login(self, username, password):
        res = self.request.post(
            "/login",
            json={
                "username": username,
                "password": password
            }
        )

        if res.status_code == 200:
            self.token = res.json().get("token")

        return res

    def get_user(self, username):
        headers = {}
        if self.token:
            headers["Authorization"] = self.token

        return self.request.get(
            f"/users/{username}",
            headers=headers
        )

    def get_profile(self):
        headers = {}
        if self.token:
            headers["Authorization"] = self.token

        return self.request.get(
            "/profile",
            headers=headers
        )