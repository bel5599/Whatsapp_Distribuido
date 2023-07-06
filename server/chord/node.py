from typing import Union
import random
import time
import sys

from .base_node import BaseNode
from ..util import generate_id


class Finger:
    def __init__(self, i: int, m: int, k: int, node: Union[BaseNode, None] = None):
        m = 2**m
        k = 2**k
        self.start = (i + k) % m
        self.end = (i + 2*k) % m

        self.node = node

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

        self.fingers: list[Finger] = [Finger(id, capacity, k, None)
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

    @staticmethod
    def _inside_interval(value: int, interval: tuple[int, int], inclusive: tuple[bool, bool] = (False, False)):
        low, up = interval

        if low == up:
            # range is all the ring
            return value != low or any(inclusive)

        if low > up:
            # if low > up, you have, for example an interval like this: {5, 3}
            # the complementary interval is !{3, 5!}
            # so checking if not in the complementary is equivalent
            low, up = up, low
            inclusive = (not inclusive[1], not inclusive[0])
            return not Node._inside_interval(value, (low, up), inclusive)

        inclusive_low, inclusive_up = inclusive

        def low_compare(
            v: int, l: int): return v >= l if inclusive_low else v > l
        def up_compare(
            v: int, u: int): return v <= u if inclusive_up else v < u

        return low_compare(value, low) and up_compare(value, up)

    def _alone(self):
        p = self == self.predecessor()
        s = p and self == self.successor()
        return s and all([finger.node and finger.node == self for finger in self.fingers])

    def network_capacity(self):
        return len(self.fingers)

    def successor(self):
        successor = self.fingers[0].node
        if successor:
            return successor

        raise Exception(f"{self} successor not found!")

    def set_successor(self, node: BaseNode):
        self.fingers[0].node = node

    def predecessor(self):
        if self._predecessor:
            return self._predecessor

        raise Exception(f"{self} predecessor not found!")

    def set_predecessor(self, node: BaseNode):
        self._predecessor = node

    def closest_preceding_finger(self, id: int):
        node = self
        for finger in self.fingers[::-1]:
            if finger.node and self._inside_interval(finger.node.id, (self.id, id)):
                node = finger.node
                break

        return node

    def find_predecessor(self, id: int):
        node = self
        while not self._inside_interval(id, (node.id, node.successor().id), (False, True)):
            node = node.closest_preceding_finger(id)

        return node

    def find_successor(self, id: int):
        return self.find_predecessor(id).successor()

    def join_network(self, node: BaseNode):
        successor = node.find_successor(self.id)

        if successor.id == self.id:
            print("A node already exists with this id")
            sys.exit(0)

        self.set_successor(successor)

    def notify(self, node: BaseNode):
        predecessor = self.predecessor()
        if (not predecessor) or self._inside_interval(node.id, (predecessor.id, self.id)):
            self.set_predecessor(node)

    def stabilize(self):
        successor = self.successor()
        node = successor.predecessor()
        if self._inside_interval(node.id, (self.id, successor.id)):
            self.set_successor(node)

        self.successor().notify(self)

    def fix_random_finger(self):
        index = random.randint(1, self.network_capacity() - 1)
        finger = self.fingers[index]

        finger.node = self.find_successor(finger.start)

    def keep_healthy(self, interval: int):
        while True:
            time.sleep(interval)

            self.stabilize()
            self.fix_random_finger()
