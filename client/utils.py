from server.node.remote_entity_node import RemoteEntityNode
from server.util import generate_id

def replication_user(inf_nodo:dict,nickname:str,password:str,ip:str,port:str):
    try:
        # nodo que va a guardar la informacion del user
        server_node_data = RemoteEntityNode(-1, inf_nodo['ip'], inf_nodo['port'])
        capacity = server_node_data.network_capacity()
        server_node_data.id = generate_id(f"{inf_nodo['ip']}:{inf_nodo['port']}", capacity)

        server_node_data.add_user(nickname,password,ip,port)
    except:
        return False,False    
    try:
        # replicar la informacion del usuario en el nodo sucesor
        dict_successor = server_node_data.successor()
        server_successor = RemoteEntityNode(-1,dict_successor.ip,dict_successor.port)
        server_successor.id = generate_id(f"{dict_successor.ip}:{dict_successor.port}", capacity)
        
        server_successor.add_user(nickname,password,ip,port,server_node_data.id)
        
        # replicar la informacion del usuario en el nodo sucesor del sucesor
        dict_successor_successor = server_successor.successor()
        server_successor_successor = RemoteEntityNode(-1,dict_successor_successor.ip,dict_successor_successor.port)
        server_successor.id = generate_id(f"{server_successor_successor.ip}:{server_successor_successor.port}", capacity)
        
        server_successor_successor.add_user(nickname,password,ip,port,server_node_data.id)
    except:
        return False,False
    
    return dict_successor,dict_successor_successor

def get_entity_data(inf_nodo):
    # nodo que va a guardar la informacion del user
    try:
        server_node_data = RemoteEntityNode(-1, inf_nodo['ip'], inf_nodo['port'])
        capacity = server_node_data.network_capacity()
        server_node_data.id = generate_id(f"{inf_nodo['ip']}:{inf_nodo['port']}", capacity)
        
    except:
        return False,False,False
    # replicar la informacion del usuario en el nodo sucesor
    try:
        dict_successor = server_node_data.successor()
        server_successor = RemoteEntityNode(-1,dict_successor.ip,dict_successor.port)
        #capacity = server_successor.network_capacity()
        server_successor.id = generate_id(f"{dict_successor.ip}:{dict_successor.port}", capacity)

        
        dict_successor_successor = server_successor.successor()
        #server_successor_successor = RemoteEntityNode(-1,dict_successor_successor.ip,dict_successor_successor.port)
    except:
        return False,False,False
    
    return server_node_data,dict_successor,dict_successor_successor

def replication_messenge(inf_nodo,source,destiny,messenge): 
    try:
        # nodo que va a guardar la informacion del user
        server_node_data = RemoteEntityNode(-1, inf_nodo['ip'], inf_nodo['port'])
        capacity = server_node_data.network_capacity()
        server_node_data.id = generate_id(f"{inf_nodo['ip']}:{inf_nodo['port']}", capacity)
        
        server_node_data.add_messenger(source,destiny,messenge)
    except:
        return False    
    try:
        # replicar la informacion del usuario en el nodo sucesor
        dict_successor = server_node_data.successor()
        server_successor = RemoteEntityNode(-1,dict_successor.ip,dict_successor.port)
        #capacity = server_successor.network_capacity()
        server_successor.id = generate_id(f"{dict_successor.ip}:{dict_successor.port}", capacity)

        server_successor.add_messenger(source,destiny,messenge,server_node_data.id)

        # replicar la informacion del usuario en el nodos antecesor
        dict_successor_successor = server_successor.successor()
        server_successor_successor = RemoteEntityNode(-1,dict_successor_successor.ip,dict_successor_successor.port)
        #capacity = server_successor_successor.network_capacity()
        server_successor.id = generate_id(f"{server_successor_successor.ip}:{server_successor_successor.port}", capacity)

        server_successor_successor.add_messenger(source,destiny,messenge,server_node_data.id)
    except:
        return False
