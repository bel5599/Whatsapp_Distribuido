from requests import get, put, delete, post
from json import dumps


class RequestManager:
    def __init__(self, ip: str, port: str, timeout: int = 5, headers: dict[str, str] = {}, secure=False):
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

        params = kwargs.get("params", None)
        if params is not None:
            kwargs["params"] = dumps(params)

        return get(f"{self._url}{route}", timeout=self._timeout, **kwargs)

    def put(self, route: str, **kwargs):
        data = kwargs.get("data", {})
        kwargs["data"] = dumps(data)

        params = kwargs.get("params", None)
        if params is not None:
            kwargs["params"] = dumps(params)

        return put(f"{self._url}{route}", timeout=self._timeout, **kwargs)

    def post(self, route: str, **kwargs):
        data = kwargs.get("data", {})
        kwargs["data"] = dumps(data)

        params = kwargs.get("params", None)
        if params is not None:
            kwargs["params"] = dumps(params)

        return post(f"{self._url}{route}", timeout=self._timeout, **kwargs)

    def delete(self, route: str, **kwargs):
        data = kwargs.get("data", {})
        kwargs["data"] = dumps(data)

        params = kwargs.get("params", None)
        if params is not None:
            kwargs["params"] = dumps(params)

        return delete(f"{self._url}{route}", timeout=self._timeout, **kwargs)
