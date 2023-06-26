from ..chord.remote_node import RemoteNode as ChordRemoteNode

class RemoteEntityNode(ChordRemoteNode):
    def __init__(self, id: int, ip: str, port: str):
        super().__init__(id, ip, port)
        