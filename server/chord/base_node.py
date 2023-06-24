class BaseNode:
    def __init__(self, id: int, ip: str, port: str):
        self.id = id
        self.ip = ip
        self.port = port

    @classmethod
    def from_dict(cls, d: dict):
        id = d.get("id", None)
        ip = d.get("ip", None)
        port = d.get("port", None)

        if id is not None and ip is not None and port is not None:
            return cls(id, ip, port)

    def to_dict(self):
        return {"id": self.id, "ip": self.ip, "port": self.port}

    def successor(self):
        raise NotImplementedError()

    def predecessor(self):
        raise NotImplementedError()

    def set_predecessor(self, node: "BaseNode"):
        raise NotImplementedError()

    def closest_preceding_finger(self, id: int):
        raise NotImplementedError()

    def find_successor(self, id: int):
        raise NotImplementedError()

    def update_finger_table(self, node: "BaseNode", index: int):
        raise NotImplementedError()
