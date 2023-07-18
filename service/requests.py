from requests import get, put, delete, post
from json import dumps
from hashlib import sha256


class RequestManager:
    def __init__(self, ip: str, port: str, timeout: int = 1, headers: dict[str, str] = {}, secure=False):
        s = "s" if secure else ""
        self.ip = ip
        self.port = port
        self._url = f"http{s}://{ip}:{port}"
        self._headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            **headers
        }
        self._timeout = timeout

    def get(self, route: str, **kwargs):
        data = kwargs.get("data", {})
        kwargs["data"] = dumps(data)
        timeout = kwargs.get("timeout", self._timeout)
        kwargs["timeout"] = timeout

        return get(f"{self._url}{route}", **kwargs)

    def put(self, route: str, **kwargs):
        data = kwargs.get("data", {})
        kwargs["data"] = dumps(data)
        timeout = kwargs.get("timeout", self._timeout)
        kwargs["timeout"] = timeout

        return put(f"{self._url}{route}", **kwargs)

    def post(self, route: str, **kwargs):
        data = kwargs.get("data", {})
        kwargs["data"] = dumps(data)
        timeout = kwargs.get("timeout", self._timeout)
        kwargs["timeout"] = timeout

        return post(f"{self._url}{route}", **kwargs)

    def delete(self, route: str, **kwargs):
        data = kwargs.get("data", {})
        kwargs["data"] = dumps(data)
        timeout = kwargs.get("timeout", self._timeout)
        kwargs["timeout"] = timeout

        return delete(f"{self._url}{route}", **kwargs)

    def __eq__(self, value: "RequestManager") -> bool:
        return self.ip == value.ip and self.port == value.port

    def __hash__(self) -> int:
        return int(sha256(self._url.encode()).hexdigest(), 16) % 2 ** 32
