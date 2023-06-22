from .base_node import BaseNode
from .remote_node import RemoteNode


def get_number_writer(key: str):
    def number_writer(data: int):
        return {key: data}

    return number_writer


id_writer = get_number_writer("id")

i_writer = get_number_writer("i")


def empty_writer(data):
    return {}


def node_writer(data: BaseNode):
    return {"id": data.id, "ip": data.ip, "port": data.port}


def remote_node_writer(d: dict): return RemoteNode.from_dict(d)


def none_writer(d: dict): return None
