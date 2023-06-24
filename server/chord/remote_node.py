from .base_node import BaseNode


class RemoteNode(BaseNode):
    def successor(self):
        pass

    def predecessor(self):
        pass

    def set_predecessor(self, node: BaseNode):
        pass

    def closest_preceding_finger(self, id: int):
        pass

    def find_successor(self, id: int):
        pass

    def update_finger_table(self, node: BaseNode, index: int):
        pass
