class BaseNode:
    def __init__(self, id: int, ip: str, port: str):
        self.id = id
        self.ip = ip
        self.port = port

    def to_dict(self):
        raise NotImplementedError()
        
    def successor(self):
        raise NotImplementedError()

    def predecessor(self):
        raise NotImplementedError()
    
    def set_predecessor(self, node: "BaseNode"):
        raise NotImplementedError()
    
    def closest_preceding_finger(self, id: int):
        raise NotImplementedError()

    def find_successor(self, id: int):
        raise NotImplementedError()

    def update_finger_table(self, node: "BaseNode", i: int):
        raise NotImplementedError()
