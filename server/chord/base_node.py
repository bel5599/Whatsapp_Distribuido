from pydantic import BaseModel


class BaseNodeModel(BaseModel):
    id: int
    ip: str
    port: str


class BaseNode:
    def __init__(self, id: int, ip: str, port: str):
        self.id = id
        self.ip = ip
        self.port = port

    @classmethod
    def from_base_model(cls, model: BaseNodeModel):
        return cls(model.id, model.ip, model.port)

    @classmethod
    def from_serialized(cls, d: dict):
        id = d.get("id", None)
        ip = d.get("ip", None)
        port = d.get("port", None)

        if id is not None and ip is not None and port is not None:
            return cls(id, ip, port)

    def serialize(self):
        return {"id": self.id, "ip": self.ip, "port": self.port}

    def network_capacity(self) -> int:
        raise NotImplementedError()

    def successor(self) -> "BaseNode":
        raise NotImplementedError()

    def predecessor(self) -> "BaseNode":
        raise NotImplementedError()

    def set_predecessor(self, node: "BaseNode") -> None:
        raise NotImplementedError()

    def closest_preceding_finger(self, id: int) -> "BaseNode":
        raise NotImplementedError()

    def find_successor(self, id: int) -> "BaseNode":
        raise NotImplementedError()

    def update_fingers(self, node: "BaseNode", index: int) -> None:
        raise NotImplementedError()
