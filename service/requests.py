from requests import get, put, delete
from json import dumps


class RequestManager:
    def __init__(self, ip: str, port: str, headers: dict[str, str] = {}, secure=False):
        s = "s" if secure else ""
        self._url = f"http{s}://{ip}:{port}"
        self._headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            **headers
        }

    def get(self, route: str, **kwargs):
        return get(f"{self._url}{route}", **kwargs)

    def put(self, route: str, **kwargs):
        data = kwargs.get("data", {})
        kwargs["data"] = dumps(data)

        return put(f"{self._url}{route}", **kwargs)

    def delete(self, route: str, **kwargs):
        return delete(f"{self._url}{route}", **kwargs)