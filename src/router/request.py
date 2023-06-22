class Request:
    def __init__(self, data):
        self.data = data

    def is_valid(self):
        return True


class RequestWriter:
    def __init__(self, payload_writer):
        self.payload_writer = payload_writer

    def write(self, type: str, data):
        result = {}
        result["type"] = type

        try:
            result["payload"] = self.payload_writer(data)
        except:
            result["payload"] = {}

        return result


class RequestReader:
    def __init__(self, payload_reader):
        self.payload_reader = payload_reader

    def read(self, request_data: dict):
        payload = request_data.get("payload", {})

        try:
            data = self.payload_reader(payload)
        except:
            data = None

        return Request(data)
