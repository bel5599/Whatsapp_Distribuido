from typing import Union

from .base_node import BaseNode
from .remote_node import RemoteNode
from ..util import get_ip, generate_id


class Finger:
    def __init__(self, m, k, node: Union[BaseNode, None] = None):
        self.start = (2**k) % (2**m)  # 2^(k) mod 2^m
        self.end = (2**(k+1)) % (2**m)  # 2^(k+1) mod 2^m
        self.node = node
        # finger[i].node = suc cessor(finger[i].start)


class Node(BaseNode):
    def __init__(self, id: int, ip: str, port: str):
        super().__init__(id, ip, port)

        self.fingers = []
        self._predecessor: Union[BaseNode, None] = None

    @classmethod
    def create_network(cls, port: str, network_capacity: int):
        ip = get_ip()
        id = generate_id(f"{ip}:{port}", network_capacity)
        node = cls(id, ip, port)

        # node is the only node in network, so:
        node.fingers = [Finger(network_capacity, k, node)
                        for k in range(network_capacity)]
        node.set_predecessor(node)

        return node

    @classmethod
    def join_network(cls, network_ip: str, network_port: str, port: str):
        # crear nodo remoto sin id, solo por comunicacion
        network_node = RemoteNode(-1, network_ip, network_port)

        # conseguir capacidad de la red para generar id
        network_capacity = network_node.network_capacity()

        network_node.id = generate_id(
            f"{network_ip}:{network_port}", network_capacity)
        # network node is ready now

        ip = get_ip()
        id = generate_id(f"{ip}:{port}", network_capacity)
        node = cls(id, ip, port)
        node.join(network_node)

        return node

    def network_capacity(self) -> int:
        return len(self.fingers)

    def successor(self):
        return self.fingers[0].node

    def predecessor(self):
        return self._predecessor

    def set_predecessor(self, node: BaseNode):
        self._predecessor = node

    def closest_preceding_finger(self, id: int):
        for finger in self.fingers[::-1]:
            if finger.node and self.id < finger.node.id < id:
                return finger.node
        return self

    def find_predecessor(self, id: int):
        node = self

        while id <= node.id or id > node.successor().id:
            node = node.closest_preceding_finger(id)

        return node

    def find_successor(self, id: int):
        node = self.find_predecessor(id)
        return node.successor()

    def update_fingers(self, node: BaseNode, i: int):
        finger_node = self.fingers[i].node

        if finger_node and self.id <= node.id < finger_node.id:
            self.fingers[i] = node
            self.predecessor().update_fingers(node, i)

    def update_others(self):
        for i in range(len(self.fingers)):
            node = self.find_predecessor(self.id - 2**i)
            node.update_fingers(self, i)

    def init_fingers(self, node: BaseNode):
        self.fingers[0].node = node.find_successor(
            self.fingers[0].start)
        self.set_predecessor(self.successor().predecessor())
        self.successor().set_predecessor(self)

        for i in range(1, len(self.fingers)):
            if self.id <= self.fingers[i].start < self.fingers[i-1].node.id:
                self.fingers[i].node = self.fingers[i-1].node
            else:
                self.fingers[i].node = node.find_successor(
                    self.fingers[i].start)

    def join(self, node: BaseNode):
        self.init_fingers(node)
        self.update_others()
