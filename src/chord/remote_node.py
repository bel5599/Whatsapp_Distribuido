import zmq

from chord.base_node import BaseNode
from chord.zmq_context import CONTEXT
from src.router import Request, RequestWriter, ResponseReader


class RemoteNode(BaseNode):
    def _remote_call(self, request: Request, timeout=2500, retries=3):
        raise NotImplementedError()

    def successor(self):
        # comunicacion por la red
        pass

    def predecessor(self):
        # comunicacion por la red
        pass

    def set_predecessor(self, node: BaseNode):
        # comunicacion por la red
        pass

    def closest_preceding_finger(self, id: int):
        # comunicacion por la red
        pass

    def find_successor(self, id: int):
        # comunicacion por la red
        pass

    def update_finger_table(self, node: "BaseNode", i: int):
        # comunicacion por la red
        pass

    @classmethod
    def from_dict(cls, d: dict):
        id = d.get("id", None)
        ip = d.get("ip", None)
        port = d.get("port", None)

        if id != None and ip != None and port != None:
            return cls(id, ip, port)
