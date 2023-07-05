from server.node.remote_entity_node import RemoteEntityNode

def replication_user(inf_nodo,nickname,password):
    # nodo que va a guardar la informacion del user
    server_node_data = RemoteEntityNode(-1, inf_nodo['ip'], inf_nodo['port'])
    server_node_data.add_user(nickname,password)
    # replicar la informacion del usuario en el nodo sucesor
    dict_successor = server_node_data.successor()
    server_successor = RemoteEntityNode(-1,dict_successor.ip,dict_successor.port)
    server_successor.add_user(nickname,password)
    # replicar la informacion del usuario en el nodo sucesor del sucesor
    dict_successor_successor = server_successor.successor()
    server_successor_successor = RemoteEntityNode(-1,dict_successor_successor.ip,dict_successor_successor.port)
    server_successor_successor.add_user(nickname,password)
    
    return dict_successor,dict_successor_successor

def get_entity_data(inf_nodo):
    # nodo que va a guardar la informacion del user
    server_node_data = RemoteEntityNode(-1, inf_nodo['ip'], inf_nodo['port'])
    # replicar la informacion del usuario en el nodo sucesor
    dict_successor = server_node_data.successor()
    server_successor = RemoteEntityNode(-1,dict_successor.ip,dict_successor.port)
    # replicar la informacion del usuario en el nodos antecesor
    dict_successor_successor = server_successor.successor()
    server_successor_successor = RemoteEntityNode(-1,dict_successor_successor.ip,dict_successor_successor.port)
    return server_node_data,dict_successor,dict_successor_successor

def replication_messenge(inf_nodo,source,destiny,messenge):
    # nodo que va a guardar la informacion del user
    server_node_data = RemoteEntityNode(-1, inf_nodo['ip'], inf_nodo['port'])
    server_node_data.add_messenger(source,destiny,messenge)
    # replicar la informacion del usuario en el nodo sucesor
    dict_successor = server_node_data.successor()
    server_successor = RemoteEntityNode(-1,dict_successor.ip,dict_successor.port)
    server_successor.add_messenger(source,destiny,messenge)
    # replicar la informacion del usuario en el nodos antecesor
    dict_successor_successor = server_successor.successor()
    server_successor_successor = RemoteEntityNode(-1,dict_successor_successor.ip,dict_successor_successor.port)
    server_successor_successor.add_messenger(source,destiny,messenge)
    return dict_successor,dict_successor_successor
