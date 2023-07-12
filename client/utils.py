from server.node.remote_entity_node import RemoteEntityNode
from server.util import generate_id
from data.database_client import DataBaseClient
from server.node.base_entity_node import BaseEntityNode 
from typing import Union

def register_user(inf_nodo: BaseEntityNode, nickname: str, password: str, ip: str, port: str):
    try:
        server_node_data = inf_nodo
        result = server_node_data.add_user(nickname, password, ip, port,-1)
        return result
    except:
        return False
    
def get_entity_data(inf_nodo: BaseEntityNode):
    # nodo que va a guardar la informacion del user
    try:
        # server_node_data = RemoteEntityNode(-1,
        #                                     inf_nodo.ip, inf_nodo.port)
        # capacity = server_node_data.network_capacity()
        # server_node_data.id = generate_id(
        #     f"{inf_nodo.ip}:{inf_nodo.port}", capacity)
        server_node_data = inf_nodo
    except:
        return False, False, False
    # replicar la informacion del usuario en el nodo sucesor
    try:
        dict_successor = server_node_data.successor()
        if dict_successor is not None:
            # server_successor = RemoteEntityNode(-1,dict_successor.ip, dict_successor.port)
            # server_successor.id = generate_id(f"{dict_successor.ip}:{dict_successor.port}", capacity)
            dict_successor_successor = dict_successor.successor()
            #dict_successor_successor = server_successor.successor()
            if dict_successor_successor is not None:    
                # server_successor_successor = RemoteEntityNode(-1, dict_successor_successor.ip, dict_successor_successor.port)
                # server_successor_successor.id = generate_id(f"{server_successor_successor.ip}:{server_successor_successor.port}", capacity)
                #return server_node_data, server_successor, server_successor_successor        
                return server_node_data,dict_successor,dict_successor_successor
            return server_node_data,dict_successor,None
        return server_node_data,None,None  
    except:
        return False, False, False


def add_messenge(inf_nodo:BaseEntityNode, source:str, destiny:str, messenge:str):
    try:
        # nodo que va a guardar la informacion del user
        # server_node_data = RemoteEntityNode(-1,
        #                                     inf_nodo.ip, inf_nodo.port)
        # capacity = server_node_data.network_capacity()
        # server_node_data.id = generate_id(
        #     f"{inf_nodo.ip}:{inf_nodo.port}", capacity)
        server_node_data = inf_nodo
        server_node_data.add_messages(source, destiny, messenge,-1)
    except:
        return False
    # try:
    #     # replicar la informacion del usuario en el nodo sucesor
    #     dict_successor = server_node_data.successor()
    #     if dict_successor is not None:
    #         server_successor = RemoteEntityNode(-1,
    #                                         dict_successor.ip, dict_successor.port)
        
    #         server_successor.id = generate_id(
    #         f"{dict_successor.ip}:{dict_successor.port}", capacity)

    #         server_successor.add_messenges(
    #             source, destiny, messenge, server_node_data.id)

    #     # replicar la informacion del usuario en el nodos antecesor
    #         dict_successor_successor = server_successor.successor()
    #         if dict_successor_successor is not None:
                
    #             server_successor_successor = RemoteEntityNode(
    #                 -1, dict_successor_successor.ip, dict_successor_successor.port)
    #     # capacity = server_successor_successor.network_capacity()
    #             server_successor_successor.id = generate_id(
    #                 f"{server_successor_successor.ip}:{server_successor_successor.port}", capacity)

    #             server_successor_successor.add_messenges(
    #                         source, destiny, messenge, server_node_data.id)
    # except:
    #     return False


def task_receive_message(nickname: str, data: DataBaseClient, server_node_data:BaseEntityNode):
    # Lista de tupla de quien lo envio, value
    messenges = server_node_data.search_messages_to(nickname,'',-1)
    # if server_successor is not None:
    #     server_successor.delete_messenges_to(nickname,server_node_data.id)
    # if server_successor_successor is not None and server_successor_successor is not False and  server_successor_successor is not True:
    #     server_successor_successor.delete_messenges_to(nickname,server_node_data.id)
    server_node_data.delete_messages_to(nickname,-1)
    
    for messenge in messenges:
        data.add_messages(messenge[0], nickname, messenge[1])
