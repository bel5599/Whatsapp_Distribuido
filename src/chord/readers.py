from remote_node import RemoteNode
from chord.base_node import BaseNode

def remote_node_reader(d: dict): return RemoteNode.from_dict(d)

def none_reader(d: dict): return None

def get_number_reader(key: str):
    def number_reader(data: int):
        return {key: data}

    return number_reader


def empty_reader(data):
    return {}


id_reader = get_number_reader("id")


def node_reader(data: BaseNode):
    return {"id": data.id, "ip": data.ip, "port": data.port}