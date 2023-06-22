from remote_node import RemoteNode
def remote_node_reader(d: dict): return RemoteNode.from_dict(d)

def none_reader(d: dict): return None