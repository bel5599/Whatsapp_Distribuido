
class BaseNode:
    def __init__():
        pass

    def successor(self):
        raise NotImplementedError()

    def predecessor(self):
        raise NotImplementedError()
    
    def closest_preceding_finger(self, id):
        raise NotImplementedError()

    def find_successor(self, id):
        raise NotImplementedError()

    def update_finger_table(self, node: BaseNode, i: int):
        raise NotImplementedError()