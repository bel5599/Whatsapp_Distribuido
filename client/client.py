from fastapi import FastAPI
# import json
# import requests
# import os
# from fastapi_utils.tasks import repeat_every
# from sqlalchemy import true
from .client_node import ClientNode
from .utils import*

client_interface = FastAPI()
client = ClientNode()


@client_interface.post("/Register")
def register(nickname: str, password: str, server: str):
    # nodo servidor de entrada
    ip = server.split(':')[0]
    port = server.split(':')[1]
    server_node = RemoteEntityNode(-1, ip, port)

    # verificar si el usuario ya esta en el sistema y validacion del servidor de entrada
    try:
        node_data = server_node.nickname_entity_node(nickname)
    except:
        return "Wrong server"
        
    if node_data.get('ip') is not None:
        return "You are already registered"
    else: # Hashear el nickname para obtener un servidor
        node_data = server_node.search_entity_node(nickname)

    # Guardar la informacion del usuario y replica la informacion
    dict_successor,dict_successor_successor = replication_user(node_data,nickname,password,client.ip,client.port)
    if dict_successor is False:
        return "Register failed"
    
    # Agrega al entity que guarda los datos del cliente, sucesor, sucesor del sucesor y por el q se conecta
    servers =[]
    servers.append(server)
    servers.append(node_data['ip']+":"+node_data['port'])
    servers.append(dict_successor.ip+":"+dict_successor.port)
    servers.append(dict_successor_successor.ip+":"+dict_successor_successor.port)
    # Loguear al usuario
    client.login_user(nickname,password,servers)
    return

@client_interface.post("/Login")
def login(nickname: str, password: str,server: str):
    if client.login:
        return 'You Are Login'
    
    # nodo servidor de entrada FALTA VALIDADCION DEL NODO
    ip = server.split(':')[0]
    port = server.split(':')[1]
    
    server_node = RemoteEntityNode(-1, ip, port)
    # verificar si el usuario ya esta en el sistema y validacion del servidor de entrada
    try:
        node_data = server_node.nickname_entity_node(nickname)
    except:
        return "Wrong server"
    
    if node_data.get('ip') is None:
        return "You are not registered"

    # obtener los nodos que tienen la informacion original y replicada del usuario
    server_node_data,dict_successor,dict_successor_successor = get_entity_data(node_data)
    if dict_successor is False:
        return "Login failed"
    
    # Verificar contrasenna y retornar una notificacion
    try:
        # verificar que no se ha caido el servidor 
        password_server =server_node_data.get_pasword(nickname,True)
        # Si cambio el ip y el port actualizar estos valores
        server_node_data.update_user(nickname,client.ip,client.port)
    except:
        return "Login failed"
             
    if password!=password_server :
        return "Wrong password"

    

    # Agrega al entity que guarda los datos del cliente, sucesor, sucesor del sucesor y por el q se conecta
    servers =[]
    servers.append(server)
    servers.append(node_data['ip']+":"+node_data['port'])
    servers.append(dict_successor.ip+":"+dict_successor.port)
    servers.append(dict_successor_successor.ip+":"+dict_successor_successor.port)
    # Loguear al usuario
    client.login_user(nickname,password,servers)
    return


#FALTA
@client_interface.post("/Logout")
def logout():
  client.logout_user()
  # Tunvar el ciente FALTA
  return

# # Permite ver los mensajes entre "my_nickname" y "nickname".
# @client_interface.get("/Messages")
# def messages(nickname: str):  # usuario de la conversacion conmigo
#     # chequear que el usuario esté loggeado
#     if not client.login:
#         return "You are not logged in"
#     # VERIFICAR QUE LOS SERVIDORES ESTEN ACTIVOS Y ACTUALIZAR LA LISTA DE SERVERS DEL USUARIO
#     #client.update_servers()
#     servers = client.server_list()
#     # server que contiene informacion
#     if len(servers)==0:
#         return 'Broken Connection, you need to exit the login and login again'
#     if len(servers)>1:
#         inf_node = servers[1]
#     else:
#     # en caso de que no haya activo o guardado un nodo que tenga su informacion
#         inf_node = servers[0]
#         search = True

#     ip = inf_node.split(':')[0]
#     port = inf_node.split(':')[1]
#     node_data = RemoteEntityNode(-1, ip, port)

#     if search: #entonces hay que buscar el nodo con iformacion del usuario
#         node_data = node_data.nickname_entity_node(client.user,True)
#         #si no se encontro un nodo con informacion del usuario
#         if node_data.get('ip') is None:
#             return "Your data has been lost"
#         # si se encontro un nodo, obtener el nodo para hacerle los pedidos
#         node_data = RemoteEntityNode(-1, node_data['ip'], node_data['port'])
#         messengers = node_data.search_chat(client.user,nickname,True)
#     else:
#         # mando a buscar los mensajes al servidor
#         messengers = node_data.search_chat(client.user,nickname)

#     # Para ver mejor los mensajes
#     messages_format = []
#     for message in messengers:
#         if message['user_id_from'] == client.user:
#             messages_format.append( 'me' + ": " + message['value'])
#         else:
#             messages_format.append(message['user_id_from'] + ": " + message['value'])
#     return messages_format

@client_interface.get("/Messages")
def messages(nickname: str):  # usuario de la conversacion conmigo
    #chequear que el usuario esté loggeado
    if not client.login:
        return "You are not logged in"
    
    servers = client.server_list()
    
    # server que contiene informacion
    if len(servers)==0:
        return 'Broken Connection, you need to exit the login and login again'
    
    nickname_other_user = nickname
    #Lista de tupla de tipo(nickname,name)
    contacts = client.get_contacts()
    for contact in contacts:
        if contact[1] == nickname:
            nickname_other_user = contact[0]
    
    messages = client.search_chat(client.user['nickname'],)        



# para enviar mensajes a otro usuario
@client_interface.post("/Send")
def send(user: str, message: str):
    # se chequea que el usuario esté loggeado
    if not client.login:
        return "You are not logged in"
    
    # VERIFICAR QUE LOS SERVIDORES ESTEN ACTIVOS Y ACTUALIZAR LA LISTA DE SERVERS DEL USUARIO
    #client.update_servers()
    servers = client.server_list()
    
    # server que contiene informacion
    if len(servers)==0:
        return 'Broken Connection, you need to exit the login and login again'

    inf_node = servers[0]
    ip = inf_node.split(':')[0]
    port = inf_node.split(':')[1]
    
    try:
        node_data = RemoteEntityNode(-1, ip, port)
    except:
        return 'Broken Connection, you need to exit the login and login again'
    
    # buscar el entity en que está almacenada la información del usuario
    dict_node_data = node_data.nickname_entity_node(client.user,True)
    if  dict_node_data.get('ip') is None:
            return "Your data has been lost"

    # buscar el entity en que está almacenada la información del otro usuario
    dict_other_user = node_data.nickname_entity_node(user,True)
    if  dict_other_user.get('ip') is None:
            return user+"is not register"

    # si la informacion de los usuarios no se guarda en la misma base datos, gurdarlo en la de el tambien
    if dict_other_user['ip']!= dict_node_data['ip'] or dict_other_user['port']!= dict_node_data['port']:
        # si su servidor está activo y no es mi mismo servidor hago lo mismo.
        if replication_messenge(dict_other_user,client.user,user,message) is False:
            return 'send failed'
    # si mi server está activo le mando el mensaje para ser escrito y replico los datos
    if replication_messenge(dict_node_data,client.user,user,message) is False:
        return 'send failed'
    return
