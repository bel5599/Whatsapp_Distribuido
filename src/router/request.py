class Request:
    def __init__(self, type: str, requester: str, payload: dict):
        self.type = type
        self.requester = requester
        self.payload = payload
