from .request import RequestReader
from .response import ResponseWriter


class Router:
    def __init__(self):
        self.handlers = {}

    def add_handler(self, handler: str, request_reader: RequestReader, response_writer: ResponseWriter):
        if not handler in self.handlers:
            self.handlers[handler] = (request_reader, response_writer)

        return self

    def route(self, request_data: dict):
        type = request_data.get("type", None)

        if type is not None:
            t = self.handlers.get(type, None)
            if t is not None:
                reader, writer = t
                return (type, reader, writer)
