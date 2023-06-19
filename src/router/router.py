class Router:
    def __init__(self):
        self.handlers = {}

    def add_handler(self, handler, payload_reader, payload_writer):
        if not handler in self.handlers:
            self.handlers[handler] = (payload_reader, payload_writer)

        return self

    def route(self, request_data: dict):
        type = request_data.get("type", None)

        if type is not None:
            t = self.handlers.get(type, None)
            if t is not None:
                reader, writer = t
                request = reader.read(request_data)
                if request.is_valid():
                    response_data = writer.write(request.data)
                    return (request.ip, request.port, response_data)
