from fastapi import FastAPI
import json
import requests
# from fastapi_utils.tasks import repeat_every
# from sqlalchemy import true
import os

from server.node.remote_entity_node import RemoteEntityNode
from .client_node import ClientNode

client_interface = FastAPI()
client = ClientNode()


@client_interface.post("/Register")
def register(nickname: str, password: str, server: str):
    # nodo servidor de entrada FALTA VALIDADCION DEL NODO
    ip = server.split(':')[0]
    port = server.split(':')[1]
    server_node = RemoteEntityNode(-1, ip, port)
    
    # verificar si el usuario ya esta en el sistema
    node_data = server_node.nickname_entity_node(nickname)
    if node_data.get('ip') is not None:
        return "You are already registered"
    else: # Hashear el nickname para obtener un servidor
        node_data = server_node.search_entity_node(nickname)
        
    # Guardar la informacion del usuario
    # nodo que va a guardar la informacion del user
    server_node_data = RemoteEntityNode(-1, node_data['ip'], node_data['port'])
    server_node_data.add_user(nickname,password)
    # replicar la informacion del usuario en el nodo sucesor
    dict_successor = server_node_data.successor()
    server_successor = RemoteEntityNode(-1,dict_successor.ip,dict_successor.port)
    server_successor.add_user(nickname,password)
    # replicar la informacion del usuario en el nodos antecesor
    dict_predecessor = server_node_data.predecessor()
    server_predecessor = RemoteEntityNode(-1,dict_predecessor.ip,dict_predecessor.port)
    server_predecessor.add_user(nickname,password)
    
    # Agrega al entity que guarda los datos del cliente, su antecesor, sucesor y por el q se conecta
    servers =[]
    servers.append(server)
    servers.append(node_data['ip']+":"+node_data['port'])    
    servers.append(dict_successor.ip+":"+dict_successor.port)
    servers.append(dict_predecessor.ip+":"+dict_predecessor.port)    
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
    # Verificar que el servidor este activo FALTA
    server_node = RemoteEntityNode(-1, ip, port)
    
    # verificar si el usuario ya esta en el sistema
    node_data = server_node.nickname_entity_node(nickname)
    if node_data.get('ip') is None:
        return "You are not registered"
    
    # Verificar contrasenna y retornar una notificacion
    server_node_data = RemoteEntityNode(-1, node_data['ip'], node_data['port'])
    if password!= server_node_data.get_pasword(nickname):
        return "Wrong password"
    
    # obtener los nodos que tienen la informacion replicada del usuario 
    dict_successor = server_node_data.successor()
    dict_predecessor = server_node_data.predecessor()
    
    # Agrega al entity que guarda los datos del cliente, su antecesor, sucesor y por el q se conecta
    servers =[]
    servers.append(server)
    servers.append(node_data['ip']+":"+node_data['port'])    
    servers.append(dict_successor.ip+":"+dict_successor.port)
    servers.append(dict_predecessor.ip+":"+dict_predecessor.port)    
    # Loguear al usuario
    client.login_user(nickname,password,servers)
    return

# permite cerrar la sesión del usuario.
@client_interface.post("/Logout")  
def logout():
  client.logout_user()
  return


# Permite ver los mensajes entre "my_nickname" y "nickname".
@client_interface.get("/Messages")
def messages(nickname: str):  # usuario de la conversacion conmigo
    # chequear que el usuario esté loggeado
    if not client.login:
        return "You are not logged in"
    # buscar un server activo en la lista de servers del user
    servers = client.server
    # VERIFICAR QUE LOS SERVIDORES ESTEN ACTIVOS
    # server que contiene su informacion original
    if len(servers)>1:
        inf_node = servers[1]
    else:        
    # en caso de que no haya activo o guardado un nodo que tenga su informacion
        inf_node = client.server[0]
        search = True
    
    ip = inf_node.split(':')[0]
    port = inf_node.split(':')[1]
    node_data = RemoteEntityNode(-1, ip, port) 
    
    if search: #entonces hay que buscar el nodo con iformacion del usuario
        node_data = node_data.nickname_entity_node(nickname)
        #si no se encontro un nodo con informacion del usuario
        if node_data.get('ip') is None:
            return "Your data has been lost"
        # si se encontro un nodo, obtener el nodo para hcerle los pedidos
        node_data = RemoteEntityNode(-1, node_data['ip'], node_data['port']) 
        
    # mando a buscar los mensajes al servidor
    messengers = node_data.search_chat(client.user,nickname)
    
    # Para ver mejor los mensajes
    messages_format = []
    for message in messengers:
        if message['user_id_from'] == client.user:
            messages_format.append( 'me' + ": " + message['value']) 
        else:
            messages_format.append(message['user_id_from'] + ": " + message['value'])  
    return messages_format
  
# para enviar mensajes a otro usuario


@client_interface.post("/Send")
def send(user: str, message: str):
    # se chequea que yo esté loggeado
    # retornar una notificacion en caso de no estarlo
    # buscar el entity en que está almacenada la información del usuario
    # busco mi lista de contactos
    # buscar el entity en que está almacenada la información del otro usuario
    # si mi server está activo le mando el mensaje para ser escrito
    # si su servidor está activo y no es mi mismo servidor hago lo mismo. Si somos del mismo server ya su info se escribió
    return
