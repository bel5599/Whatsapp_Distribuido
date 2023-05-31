class Message:
    def __init__(self, type: str):
        self._type = type

    def read(self, json_dict: dict):
        pass

    def write(self, payload):
        return {
            "type": self._type,
            "payload": payload
        }


RESPONSE_SUFFIX = "_resp"


def is_valid_response(res_message: str, req_message: str):
    return res_message == f"{req_message}{RESPONSE_SUFFIX}"
