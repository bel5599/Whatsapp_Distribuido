class Request:
    def __init__(self, requester: dict, data):
        self.requester = requester
        self.data = data

    def is_valid(self):
        if self.data:
            ip = self.requester.get("ip", "")
            port = self.requester.get("port", "")
            return ip != "" and port != ""

        return False


class RequestWriter:
    def __init__(self, payload_writer):
        self.payload_writer = payload_writer

    def write(self, type: str, ip: str, port: str, data):
        result = {}
        result["type"] = type
        result["requester"] = {"ip": ip, "port": port}

        try:
            result["payload"] = self.payload_writer(data)
        except:
            result["payload"] = {}

        return result


class RequestReader:
    def __init__(self, payload_reader):
        self.payload_reader = payload_reader

    def read(self, request_data: dict):
        requester = request_data.get("requester", {})
        payload = request_data.get("payload", {})

        try:
            data = self.payload_reader(payload)
        except:
            data = None

        return Request(requester, data)
