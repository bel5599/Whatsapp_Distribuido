import random

class Finger:
    def __init__(self, m, k, node = None):
        self.start = (2**k) % (2**m) # 2^(k) mod 2^m
        self.end =  (2**(k+1)) % (2**m) #2^(k+1) mod 2^m
        self.node = node
        # finger[i].node = suc cessor(finger[i].start)


class Node:
    def __init__(self, id: int, dir, port, keys, storage, transport, m):
        
        self.dir = dir
        self.port = port
        self.id = id

        self.keys = keys

        self._predecessor = find_predecessor(id)

        self.finger_table = [Finger(m, k) for k in range(m)]

        self.storage = storage
        self.transport = transport 
        self.m = m

    @property
    def succesor(self):
        return self.finger_table[0].node

    @property.setter
    def succesor(self, node_info):
        pass

    @property
    def predecessor(self):
        return self._predecessor

    @property.setter
    def predecessor(self, node_info):
        pass

    def closest_preceding_finger(self, id: int):
        for finger in self.finger_table[::-1]:
            if finger.node and self.id < finger.node.id < id:
                return finger.node.id
        return self.id

    def find_predecessor(self, id: int):
        n = self.id
        while n.id > id > n.succesor.id:
            n = n.closest_preceding_finger(id)
        return n.id

    def find_successor(self, id: int):
        n = find_predecessor(id)
        return n.succesor

    @classmethod
    def join(cls, node):
        pass
        # if node:
        #     self.init_finger_table(node)
        #     self.update_others()
        # else:
        #     for finger in self.finger_table[::-1]:
        #         finger.node.id = self.id
            

    def init_finger_table(self, node):
        self.fingerTable[1].node = node.find_successor(self.fingerTable[1].start)
        successor = self.fingerTable[1].node
        predecessor = successor.predecessor
        successor.predecessor = node
        predecessor.successor = node
        for i in range(1, m-1):
            if self.fingerTable[i+1].start in (self, self.fingerTable[i].node):
                self.fingerTable[i+1].node = self.fingerTable[i].node
            else:
                self.fingerTable[i+1].node = node.findSuccessor(self.fingerTable[i+1].start)

    def update_others(self):
        for i in range(1, self.m):
            pred = self.findPredecessor(2**m - 2**(i-1))# n - 2^(i-1)
            pred.updateFingerTable(self, i)

    def update_finger_table(self, node, i):
        if node in (self, self.fingerTable[i].node):
            self.fingerTable[i].node = node
            p = self.predecessor
            p.updateFingerTable(node, i)

    # def stabilize(self):
    #     x = self.succesor.predecessor
    #     if x in (self, self.succesor):
    #         self.succesor = x
    #     self.succesor.notify(self)

    # def notify(self, node):
    #     if (self.predecessor is None) or (node in (self.predecessor, self)):
    #         self.predecessor = node

    # def fix_fingers(self):
    #     i = random.Random()
    #     self.fingerTable[i].node = self.findSuccessor(self.fingerTable[i].start)

class NodeInfo:
    def __init__(self, id: int, dir, port):
        self.id = id
        self.dir = dir
        self.port = port

    property
    def succesor(self):
        pass

    @property.setter
    def succesor(self, node_info):
        pass

    @property
    def predecessor(self):
        pass

    @property.setter
    def predecessor(self, node_info):
        pass

    def update_finger_table(self, node_info, i: int):
        #comunicacion por la red
        pass

    def find_successor(self, id):
        #comunicacion por la red
        pass

    