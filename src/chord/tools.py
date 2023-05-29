import random

class FingerEntry:
    def __init__(self, id, node):
        self.id = id
        self.node = node

    #Revisarrrrrrrrrrrrrrrrrrrr
    def fingerTable(self, node, m):
        ft = make()
        for i in range(ft):
            ft[i] = FingerEntry(fingerId(node.id, i, m), node)
        return ft

    #Revisarrrrrrrrrrrrrrrrrrrr
# def fingerEntry(id_list, node):
#     return FingerEntry(id, node)

# def fingerID(n_list, i, m):
#     idInt = 

#Node n contains m entries in its finger table.
# successor → next node on the identifier circle
# predecessor → node on the identifier circle
# The ith finger contains:
# finger[i].start = (n + 2i−1) mod 2m,(1 ≤ i ≤ m)
# finger[i].end = (n + 2i − 1) mod 2m
# finger[i].node = successor(finger[i].start)

class Finger:
    def __init__(self, m, k, node = None):
        self.start = (2**k) % (2**m) # 2^(k) mod 2^m
        self.end =  (2**(k+1)) % (2**m) #2^(k+1) mod 2^m
        self.node = node
        # finger[i].node = suc cessor(finger[i].start)



class Node:
    def __init__(self, dir, port, keys, storage, transport, m):
        
        self.dir = dir
        self.port = port

        self.keys = keys

        self.predecessor = find_predecessor(id)
        self.succesor = find_successor(id)

        self.finger_table = [Finger(m, k) for k in range(m)]

        self.storage = storage
        self.transport = transport 
        self.m = m

    def find_successor(self, id):
        n = findPredecessor(id)
        return n.succesor(id)

    def find_predecessor(self, id):
        n = self
        while not id in (n, n.successor()):
            n = n.closestPrecedingFinger(id)
    
    def closest_preceding_finger(self, id):
        for i in range(self.m, 1):
            if self.fingerTable[i].node in (self, id):
                return self.fingerTable[i].node
        return self
    
    def join(self, node):
        self.initFingerTable(node)
        self.updateOthers()

    def init_finger_table(self, node):
        self.fingerTable[1].node = node.findSuccessor(self.fingerTable[1].start)
        successor = self.fingerTable[1].node
        predecessor = successor.predecessor
        successor.predecessor = node
        predecessor.successor = node
        for i in range(1, m-1):
            if self.fingerTable[i+1].start in (self, self.fingerTable[i].node):
                self.fingerTable[i+1].node = self.fingerTable[i].node
            else:
                self.fingerTable[i+1].node = node.findSuccessor(self.fingerTable[i+1].start)

    def updateOthers(self):
        for i in range(1, self.m):
            pred = self.findPredecessor(2**m - 2**(i-1))# n - 2^(i-1)
            pred.updateFingerTable(self, i)

    def update_finger_table(self, node, i):
        if node in (self, self.fingerTable[i].node):
            self.fingerTable[i].node = node
            p = self.predecessor
            p.updateFingerTable(node, i)

    def stabilize(self):
        x = self.succesor.predecessor
        if x in (self, self.succesor):
            self.succesor = x
        self.succesor.notify(self)

    def notify(self, node):
        if (self.predecessor is None) or (node in (self.predecessor, self)):
            self.predecessor = node

    def fix_fingers(self):
        i = random.Random()
        self.fingerTable[i].node = self.findSuccessor(self.fingerTable[i].start)

class NodeInfo:
    def __init__(self, id, dir, port):
        self.id = id
        self.dir = dir
        self.port = port