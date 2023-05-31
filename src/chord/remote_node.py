import zmq

from chord.zmq_context import CONTEXT
from message import Message, is_valid_response


class GetRemoteNodeMessage(Message):
    def __init__(self, type):
        super().__init__(type)

    def read(self, json_dict: dict):
        response_type = json_dict.get("type", "")
        success = json_dict.get("success", False)

        if is_valid_response(response_type, self._type) and success:
            payload = json_dict.get("payload", {})
            return RemoteNode.from_dict(payload)


class SetRemoteNodeMessage(Message):
    def __init__(self, type: str):
        super().__init__(type)

    def read(self, json_dict: dict):
        response_type = json_dict.get("type", "")
        success = json_dict.get("success", False)

        return is_valid_response(response_type, self._type) and success


class RemoteNode:
    GET_SUCCESSOR = GetRemoteNodeMessage("get_successor")
    GET_PREDECESSOR = GetRemoteNodeMessage("get_predecessor")
    SET_PREDECESSOR = SetRemoteNodeMessage("set_predecessor")

    def __init__(self, id: int, ip: str, port: str):
        self.id = id
        self.ip = ip
        self.port = port

    def _remote_call(self, payload, message: Message, timeout=2500, retries=3):
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

    @property
    def succesor(self):
        return self._remote_call({}, self.GET_SUCCESSOR)

    @property
    def predecessor(self):
        return self._remote_call({}, self.GET_PREDECESSOR)

    @property.setter
    def predecessor(self, remote_node):
        return self._remote_call(remote_node.to_dict(), self.SET_PREDECESSOR)

    def update_finger_table(self, remote_node, index: int):
        # comunicacion por la red
        pass

    def find_successor(self, id):
        # comunicacion por la red
        pass

    def to_dict(self):
        return {"id": self.id, "ip": self.ip, "port": self.port}

    @classmethod
    def from_dict(cls, d: dict):
        id = d.get("id", None)
        ip = d.get("ip", None)
        port = d.get("port", None)

        if id != None and ip != None and port != None:
            return cls(id, ip, port)
