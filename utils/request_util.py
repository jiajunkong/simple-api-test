import requests


class RequestUtil:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def send_request(self, method, url, **kwargs):
        full_url = self.base_url + url

        print("\n========== 接口请求 ==========")
        print(f"请求方法：{method.upper()}")
        print(f"请求地址：{full_url}")
        print(f"请求参数：{kwargs}")

        response = self.session.request(method, full_url, **kwargs)

        print("========== 接口响应 ==========")
        print(f"响应状态码：{response.status_code}")
        try:
            print(f"响应内容：{response.json()}")
        except Exception:
            print(f"响应内容：{response.text}")
        print("==============================")

        return response

    def get(self, url, **kwargs):
        return self.send_request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.send_request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.send_request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.send_request("DELETE", url, **kwargs)