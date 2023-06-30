from typing import Union

from .base_node import BaseNode
from ..util import generate_id


class Finger:
    def __init__(self, m, k, node: Union[BaseNode, None] = None):
        self.start = (2**k) % (2**m)  # 2^(k) mod 2^m
        self.end = (2**(k+1)) % (2**m)  # 2^(k+1) mod 2^m
        self.node = node
        # finger[i].node = suc cessor(finger[i].start)


class Node(BaseNode):
    def __init__(self, ip: str, port: str, capacity: int):
        id = generate_id(f"{ip}:{port}", capacity)
        super().__init__(id, ip, port)

        self.fingers: list[Finger] = [Finger(capacity, k, None)
                                      for k in range(capacity)]
        self._predecessor: Union[BaseNode, None] = None

    @classmethod
    def create_network(cls, ip: str, port: str, network_capacity: int):
        node = cls(ip, port, network_capacity)

        # node is the only node in network, so:
        for finger in node.fingers:
            finger.node = node
        node.set_predecessor(node)

        return node

    def network_capacity(self):
        return len(self.fingers)

    def successor(self):
        successor = self.fingers[0].node
        if successor:
            return successor

        raise Exception(f"{self}' successor not found!")

    def predecessor(self):
        if self._predecessor:
            return self._predecessor

        raise Exception(f"{self}'s predecessor not found!")

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

    def update_fingers(self, node: BaseNode, index: int):
        finger_node = self.fingers[index].node

        if finger_node and self.id <= node.id < finger_node.id:
            self.fingers[index].node = node
            self.predecessor().update_fingers(node, index)

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
            prev_node = self.fingers[i-1].node
            if prev_node and self.id <= self.fingers[i].start < prev_node.id:
                self.fingers[i].node = prev_node
            else:
                self.fingers[i].node = node.find_successor(
                    self.fingers[i].start)

    def join_network(self, node: BaseNode):
        self.init_fingers(node)
        self.update_others()
