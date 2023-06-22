import zmq

from chord.base_node import BaseNode
from chord.zmq_context import CONTEXT
from chord.utils import get_requester
from ..router import RequestWriter, ResponseReader
from chord.readers import remote_node_reader, none_reader
from chord.writers import empty_writer, node_writer, id_writer, i_writer


class RemoteNode(BaseNode):
    def _remote_call(self, type: str, data, writer: RequestWriter, timeout=2500, retries=3):
        endpoint = f"tcp://{self.ip}:{self.port}"

        requester_ip, requester_port = get_requester()
        request_data = writer.write(type, requester_ip, requester_port, data)

        client = CONTEXT.socket(zmq.REQ)
        client.connect(endpoint)
        client.send_json(request_data)

        while retries > 0:
            if (client.poll(timeout) & zmq.POLLIN) != 0:
                response_data = client.recv_json()
                if isinstance(response_data, dict):
                    return response_data

            retries -= 1
            client.setsockopt(zmq.LINGER, 0)
            client.close()

            client = CONTEXT.socket(zmq.REQ)
            client.connect(endpoint)
            client.send_json(request_data)

    def successor(self):
        type = "successor"
        data = {}
        writer = RequestWriter(empty_writer)

        response_data = self._remote_call(type, data, writer)

        reader = ResponseReader(remote_node_reader)
        return reader.read(response_data)

    def predecessor(self):
        type = "predecessor"
        data = {}
        writer = RequestWriter(empty_writer)

        response_data = self._remote_call(type, data, writer)

        reader = ResponseReader(remote_node_reader)
        return reader.read(response_data)

    def set_predecessor(self, node: BaseNode):
        type = "set_predecessor"
        data = node
        writer = RequestWriter(node_writer)

        response_data = self._remote_call(type, data, writer)

        reader = ResponseReader(none_reader)
        return reader.read(response_data)

    def closest_preceding_finger(self, id: int):
        type = "closest_preceding_finger"
        data = id
        writer = RequestWriter(id_writer)

        response_data = self._remote_call(type, data, writer)

        reader = ResponseReader(remote_node_reader)
        return reader.read(response_data)

    def find_successor(self, id: int):
        type = "find_successor"
        data = id
        writer = RequestWriter(id_writer)
        response_data = self._remote_call(type, data, writer)

        reader = ResponseReader(remote_node_reader)
        return reader.read(response_data)

    def update_finger_table(self, node: BaseNode, i: int):
        type = "update_finger_table"
        data = [node, i]

        def payload_writer(data: list):
            node_dict = node_writer(data[0])
            i_dict = i_writer(data[1])
            return {**i_dict, "node": node_dict}
        writer = RequestWriter(payload_writer)

        response_data = self._remote_call(type, data, writer)

        reader = ResponseReader(none_reader)
        return reader.read(response_data)

    @classmethod
    def from_dict(cls, d: dict):
        id = d.get("id", None)
        ip = d.get("ip", None)
        port = d.get("port", None)

        if id != None and ip != None and port != None:
            return cls(id, ip, port)
