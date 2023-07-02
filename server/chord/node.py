from typing import Union
from logging import info as log_info, error as log_error

from .base_node import BaseNode
from ..util import generate_id


class Finger:
    def __init__(self, m, k, node: Union[BaseNode, None] = None):
        self.start = (2**k) % (2**m)  # 2^(k) mod 2^m
        self.end = (2**(k+1)) % (2**m)  # 2^(k+1) mod 2^m
        self.node = node
        # finger[i].node = suc cessor(finger[i].start)

    def serialize(self):
        return {
            "start": self.start,
            "end": self.end,
            "node": self.node.serialize() if self.node else {}
        }


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
        log_info(f"getting network capacity from {self}...")
        return len(self.fingers)

    def successor(self):
        log_info(f"getting {self} successor...")

        successor = self.fingers[0].node
        if successor:
            log_info(f"{self} successor found: {successor}")
            return successor

        error_msg = f"{self} successor not found!"
        log_error(error_msg)
        raise Exception(error_msg)

    def predecessor(self):
        log_info(f"getting {self} predecessor...")

        if self._predecessor:
            log_info(f"{self} predecessor found: {self._predecessor}")
            return self._predecessor

        error_msg = f"{self} predecessor not found!"
        log_error(error_msg)
        raise Exception(error_msg)

    def set_predecessor(self, node: BaseNode):
        log_info(f"setting {self} predecessor...")
        self._predecessor = node
        log_info(f"successfully setted {self} predecessor: {node}")

    def closest_preceding_finger(self, id: int):
        log_info(f"getting {self} closest preceding finger of '{id}'...")

        node = self
        for finger in self.fingers[::-1]:
            if finger.node and self.id < finger.node.id < id:
                node = finger.node
                break

        log_info(f"{self} closest preceding finger of '{id}' is: {node}")
        return node

    def find_predecessor(self, id: int):
        log_info(f"finding '{id}' predecessor from {self}...")

        node = self
        while id <= node.id or id > node.successor().id:
            node = node.closest_preceding_finger(id)

        log_info(f"'{id}' predecessor from {self}: {node}")
        return node

    def find_successor(self, id: int):
        log_info(f"finding '{id}' successor from {self}...")

        node = self.find_predecessor(id).successor()

        log_info(f"'{id}' successor from {self}: {node}")
        return node

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



