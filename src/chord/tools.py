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
def fingerEntry(id_list, node):
    return FingerEntry(id, node)

def fingerID(n_list, i, m):
    idInt = 

class Node:
    def __init__(self, node, predecessor, succesor, fingerTable, storage, transport):
        self.node = node
        self.predecessor = predecessor
        self.succesor = succesor
        self.fingerTable = fingerTable
        self.storage = storage
        self.transport = transport

    def findSuccessor(self, id):
        n = findPredecessor(id)
        return n.succesor(id)

    def findPredecessor(self, id):
        n = self
        while not id in (n, n.successor()):
            n = n.closestPrecedingFinger(id)
    
    def closestPrecedingFinger(self, id):
        for i in range(1):
            if self.fingerTable[i].node in (self, id):
                return self.fingerTable[i].node
        return self
    
    def join(self, node):
        self.initFingerTable(node)
        self.updateOthers()

    def initFingerTable(self, node):
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
        for i in range(1, m):
            pred = self.findPredecessor(self)# n - 2^(i-1)
            pred.updateFingerTable(self, i)

    def updateFingerTable(self, node, i):
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