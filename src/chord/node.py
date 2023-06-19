from typing import Union

from chord.base_node import BaseNode
from chord.remote_node import RemoteNode
from chord.utils import generate_id


class Finger:
    def __init__(self, m, k, node: Union[BaseNode, None] = None):
        self.start = (2**k) % (2**m)  # 2^(k) mod 2^m
        self.end = (2**(k+1)) % (2**m)  # 2^(k+1) mod 2^m
        self.node = node
        # finger[i].node = suc cessor(finger[i].start)


class Node(BaseNode):
    def __init__(self, id: int, ip: str, port: str):
        super().__init__(id, ip, port)

        self.finger_table = []
        self._predecessor: Union[BaseNode, None] = None

    @classmethod
    def create_network(cls, port: str, network_capacity: int):
        ip = None  # conseguir ip
        id = None  # by hashing ip + port
        node = cls(id, ip, port)

        # node is the only node in network, so:
        node.finger_table = [Finger(network_capacity, k, node)
                             for k in range(network_capacity)]
        node.set_predecessor(node)

        return node

    @classmethod
    def join_network(cls, network_ip: str, network_port: str, ip: str, port: str):
        # crear nodo remoto sin id, solo por comunicacion
        network_node = RemoteNode(-1, network_ip, network_port)

        # conseguir capacidad de la red para generar id
        network_capacity = None  # ver como se consigue

        network_node.id = generate_id(network_ip, network_capacity)
        # network node is ready now

        id = generate_id(ip, network_capacity)
        node = cls(id, ip, port)
        node.join(network_node)

        return node

    def successor(self):
        return self.finger_table[0].node

    def predecessor(self):
        return self._predecessor

    def set_predecessor(self, node: BaseNode):
        self._predecessor = node

    def closest_preceding_finger(self, id: int):
        for finger in self.finger_table[::-1]:
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

    def update_finger_table(self, node: BaseNode, i: int):
        finger_node = self.finger_table[i].node

        if finger_node and self.id <= node.id < finger_node.id:
            self.finger_table[i] = node
            self.predecessor().update_finger_table(node, i)

    def update_others(self):
        for i in range(len(self.finger_table)):
            node = self.find_predecessor(self.id - 2**i)
            node.update_finger_table(self, i)

    def init_finger_table(self, node: BaseNode):
        self.finger_table[0].node = node.find_successor(
            self.finger_table[0].start)
        self.set_predecessor(self.successor().predecessor())
        self.successor().set_predecessor(self)

        for i in range(1, len(self.finger_table)):
            if self.id <= self.finger_table[i].start < self.finger_table[i-1].node.id:
                self.finger_table[i].node = self.finger_table[i-1].node
            else:
                self.finger_table[i].node = node.find_successor(
                    self.finger_table[i].start)

    def join(self, node: BaseNode):
        self.init_finger_table(node)
        self.update_others()
