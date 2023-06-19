import zmq

from chord.base_node import BaseNode
from chord.zmq_context import CONTEXT


class RemoteNode(BaseNode):
    def _remote_call(self, payload, message, timeout=2500, retries=3):
        endpoint = f"tcp://{self.ip}:{self.port}"

        data = message.write(payload)

        client = CONTEXT.socket(zmq.REQ)
        client.connect(endpoint)
        client.send_json(data)

        while retries > 0:
            if (client.poll(timeout) & zmq.POLLIN) != 0:
                reply = message.read(client.recv_json())
                if isinstance(reply, dict):
                    reply_data = message.read(reply)
                    if reply_data != None:
                        return reply_data

            retries -= 1
            client.setsockopt(zmq.LINGER, 0)
            client.close()

            client = CONTEXT.socket(zmq.REQ)
            client.connect(endpoint)
            client.send_json(data)

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
