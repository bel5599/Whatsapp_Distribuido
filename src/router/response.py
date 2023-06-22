class Response:
    def __init__(self, success: bool, data):
        self.success = success
        self.data = data

    def is_valid(self):
        return self.success


class ResponseWriter:
    def __init__(self, payload_writer):
        self.payload_writer = payload_writer

    def write(self, data):
        result = {}

        try:
            result["success"] = True
            # funci\'on que transforma la data
            payload = self.payload_writer(data)
            result["payload"] = payload
            pass
        except:
            result["success"] = False
            result["payload"] = {}

        return result


class ResponseReader:
    def __init__(self, payload_reader):
        self.payload_reader = payload_reader

    def read(self, response_data: dict):
        success = response_data.get("success", False)
        payload = response_data.get("payload", {})

        try:
            data = self.payload_reader(payload)
        except:
            data = None

        return Response(success, data)
