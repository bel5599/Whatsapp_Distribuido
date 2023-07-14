from data.database_client import DataBaseClient
from server.node.base_entity_node import BaseEntityNode

SERVER_ADDRESSES_CACHE_FILENAME = "server_addresses_cache.json"


def register_user(inf_nodo: BaseEntityNode, nickname: str, password: str, ip: str, port: str):
    try:
        result = inf_nodo.add_user(nickname, password, ip, port, -1)
        return result
    except:
        return False


def get_entity_data(inf_nodo: BaseEntityNode):
    try:
        dict_successor = inf_nodo.successor()
        if dict_successor is not None:
            dict_successor_successor = dict_successor.successor()
            if dict_successor_successor is not None:
                return inf_nodo, dict_successor, dict_successor_successor
            return inf_nodo, dict_successor, None
        return inf_nodo, None, None
    except:
        return False, False, False


def add_messenge(inf_nodo: BaseEntityNode, source: str, destiny: str, messenge: str):
    try:
        inf_nodo.add_messages(source, destiny, messenge, -1)
    except:
        return False


def task_receive_message(nickname: str, data: DataBaseClient, server_node_data: BaseEntityNode):
    # Lista de tupla de quien lo envio, value
    messenges = server_node_data.search_messages_to(nickname, -1)
    # replica a los sucesores desd eel entity
    server_node_data.delete_messages_to(nickname, -1)

    for messenge in messenges:
        data.add_messages(messenge[0], nickname, messenge[1])
