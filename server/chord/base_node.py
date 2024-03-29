from pydantic import BaseModel
from typing import Union


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

    def successor(self) -> Union["BaseNode", None]:
        raise NotImplementedError()

    def set_successor(self, node: "BaseNode") -> None:
        raise NotImplementedError()

    def predecessor(self) -> Union["BaseNode", None]:
        raise NotImplementedError()

    def set_predecessor(self, node: "BaseNode") -> None:
        raise NotImplementedError()

    def closest_preceding_finger(self, id: int) -> Union["BaseNode", None]:
        raise NotImplementedError()

    def find_successor(self, id: int) -> Union["BaseNode", None]:
        raise NotImplementedError()

    def notify(self, node: "BaseNode") -> None:
        raise NotImplementedError()

    def heart(self) -> Union[str, None]:
        raise NotImplementedError()

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id})"

    def __eq__(self, other: Union["BaseNode", None]):
        if not other:
            return False

        return self.id == other.id and self.ip == other.ip and self.port == other.port
    
    def __hash__(self) -> int:
        return self.id

    def __ne__(self, other: Union["BaseNode", None]):
        return not self.__eq__(other)
