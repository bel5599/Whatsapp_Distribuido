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
    
    # nodo que va a guardar la informacion del user
    # Hashear el nickname para obtener un servidor
    node_data = server_node.nickname_entity_node(nickname)
    
    # Registrar los datos del usuario FALTA VERIFICAR SI EL USUARIO YA ESTA EN EL SISTEMA
    server_node_data = RemoteEntityNode(-1, node_data['ip'], node_data['port'])
    server_node_data.add_user(nickname,password)
    list_servers = server_node_data.fingers_predecessor_list()
    
    # Agrega al entity que guarda los datos del cliente, su antecesor y los de su fingertable 
    servers =[]
    servers.append(node_data['ip']+":"+node_data['port'])
    for entity in list_servers:
        servers.append(entity['ip']+":"+entity['port'])
        
        # Agrega los datos del usuario para replicacion en los antecesores y fingertable
        entity_node = RemoteEntityNode(-1,entity['ip'], entity['port'])
        entity_node.add_user(nickname,password)
    
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
    
    # Hashear el nickname para obtener un servidor
    node_data = server_node.nickname_entity_node(nickname)
    
    server_node_data = RemoteEntityNode(-1, node_data['ip'], node_data['port'])
    
    # Luego obetener la informacion del usuario
    # Verificar contrasenna y retornar una notificacion
    # Guardar datos de logueo en una mini cachet para saber si un usuario esta logueado
    return

# Permite ver los mensajes entre "my_nickname" y "nickname".


@client_interface.get("/Messages")
def messages(nickname: str):  # usuario de la conversacion conmigo
    # chequear que el usuario esté loggeado
    # retornar una notificacion en caso de no estarlo
    # buscar el entity en que está almacenada la información del usuario
    # verificar si tengo entre mis contactos a la persona de la cual quiero ver los mensajes que tenemos
    # mando a buscar los mensajes al servidor
    return

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
