from fastapi import FastAPI
import requests
# import json
# import os
# from fastapi_utils.tasks import repeat_every
# from sqlalchemy import true
from .client_node import ClientNode
from .utils import *

service = FastAPI(docs_url=None)
client_interface = FastAPI()
client = ClientNode()


@client_interface.post("/Register")
def register(nickname: str, password: str, server: str):
    # nodo servidor de entrada
    ip = server.split(':')[0]
    port = server.split(':')[1]
    server_node = RemoteEntityNode(-1, ip, port)
    capacity = server_node.network_capacity()
    server_node.id = generate_id(
        f"{server_node.ip}:{server_node.port}", capacity)

    # verificar si el usuario ya esta en el sistema y validacion del servidor de entrada
    try:
        node = server_node.search_entity_node(nickname)
    except:
        return "Wrong server"

    node_data: Union[BaseEntityNode, None] = None

    if node is not None:
        node_data = node.nickname_entity_node(nickname, -1)
        if node_data is not None:
            return "You are already registered"
        else:  # Hashear el nickname para obtener un servidor
            node_data = node

    servers = []
    # Guardar la informacion del usuario
    if node_data is not None:
        success = register_user(node_data, nickname,
                                password, client.ip, client.port)

        if success is False:
            return "Register failed"

        server_node_data, dict_successor, dict_successor_successor = get_entity_data(
            node_data)

        # Agregar el entity que guarda los datos del cliente, sucesor, sucesor del sucesor y por el q se conecta al cliente
        servers.append(server)
        servers.append(node_data.ip+":"+node_data.port)
        # if dict_successor is not False and dict_successor is not None:
        #     servers.append(dict_successor.ip+":"+dict_successor.port)
        # if dict_successor_successor is not None and dict_successor_successor is not False:
        #     servers.append(dict_successor_successor.ip +
        #                    ":"+dict_successor_successor.port)
    # Loguear al usuario
    client.login_user(nickname, password, servers)
    return


@client_interface.post("/Login")
def login(nickname: str, password: str, server: str):
    if client.login:
        return 'You Are Login'

    # nodo servidor de entrada FALTA VALIDADCION DEL NODO
    ip = server.split(':')[0]
    port = server.split(':')[1]
    server_node = RemoteEntityNode(-1, ip, port)
    capacity = server_node.network_capacity()
    server_node.id = generate_id(
        f"{server_node.ip}:{server_node.port}", capacity)

    # verificar si el usuario ya esta en el sistema y validacion del servidor de entrada
    try:
        node_data = server_node.nickname_entity_node(nickname, -1)
    except:
        return "Wrong server"

    if node_data is None:
        return "You are not registered"

    # obtener los nodos que tienen la informacion original y replicada del usuario
    server_node_data, server_successor, server_successor_successor = get_entity_data(
        node_data)

    if server_successor is False:
        return "Login failed"

        # verificar que no se ha caido el servidor
    if server_node_data is not False:
        try:
            # Verificar contrasenna y retornar una notificacion
            password_server = server_node_data.get_pasword(nickname, -1)
            if password_server is not None and password != password_server:
                return "Wrong password"

            # Si cambio el ip y el port actualizar estos valores y actualizar en los sucessores
            server_node_data.update_user(nickname, client.ip, client.port, -1)

            # Recivo los sms que tenia en espera
            task_receive_message(client.user['nickname'], client.database,
                                 server_node_data)
            # Agrega al entity que guarda los datos del cliente, sucesor, sucesor del sucesor y por el q se conecta
            servers = []
            servers.append(server)
            servers.append(node_data.ip+":"+node_data.port)
            if server_successor is not None:
                servers.append(server_successor.ip+":"+server_successor.port)
            if server_successor_successor is not None and server_successor_successor is not False:
                servers.append(str(server_successor_successor.ip) +
                               ":"+server_successor_successor.port)
            # Loguear al usuario
            client.login_user(nickname, password, servers)
            return
        except:
            return "Login failed"

# FALTA


@client_interface.post("/Logout")
def logout():
    client.logout_user()
    # quitar el ciente FALTA
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
    # chequear que el usuario esté loggeado
    if not client.login:
        return "You are not logged in"

    # VERIFICAR QUE LOS SERVIDORES ESTEN ACTIVOS Y ACTUALIZAR LA LISTA DE SERVERS DEL USUARIO
    servers = client.server_list()

    # server que contiene informacion
    if len(servers) == 0:
        return 'Broken Connection, you need to exit the login and login again'

    nickname_other_user = client.get_nickname(nickname)
    # Si no encontro ningun contacto con ese nombre
    if nickname_other_user is None:
        nickname_other_user = nickname

    # # Lista de tupla de tipo(nickname,name)
    # contacts = client.get_contacts()
    # for contact in contacts:
    #     # si nickname es el nombre del contacto, actualizo el nickname del otro usuario
    #     if contact[1] == nickname:
    #         nickname_other_user = contact[0]

    mynickname = client.user['nickname']
    # Obtengo los sms de mi basedatos
    messenges = client.search_chat(nickname_other_user)

    # Para ver mejor los mensajes
    messages_format = []
    for message in messenges:
        if message[0] == mynickname:
            messages_format.append('me' + ": " + message[1])
        else:
            messages_format.append(
                nickname_other_user + ": " + message[1])
    return messages_format


# para enviar mensajes a otro usuario
@client_interface.post("/SendMessage")
def send(user: str, message: str):
    # se chequea que el usuario esté loggeado
    if not client.login:
        return "You are not logged in"

    # VERIFICAR QUE LOS SERVIDORES ESTEN ACTIVOS Y ACTUALIZAR LA LISTA DE SERVERS DEL USUARIO
    # client.update_servers()
    servers = client.server_list()

    # server que contiene informacion
    if len(servers) == 0:
        return 'Broken Connection, you need to exit the login and login again'
    nickname_user = client.get_nickname(user)
    if nickname_user is None:
        nickname_user = user
    # contacts = get_contacts()
    # if contacts != "You are not logged in":
    #     if user in contacts and contacts.get(user) is not None:
    #         nickname_user = str(contacts.get(user))

    inf_node = servers[0]
    ip = inf_node.split(':')[0]
    port = inf_node.split(':')[1]

    try:
        node_data = RemoteEntityNode(-1, ip, port)
        capacity = node_data.network_capacity()
        node_data.id = generate_id(f"{ip}:{port}", capacity)

    except:
        return 'Broken Connection, you need to exit the login and login again'

    # buscar el entity en que está almacenada la información del otro usuario

    dict_other_user = node_data.nickname_entity_node(nickname_user, -1)
    if dict_other_user is None:
        return user+"is not register"

    my_nickname = client.user['nickname']

    try:
        server_other_user = RemoteEntityNode(-1,
                                             dict_other_user.ip, dict_other_user.port)
        server_other_user.id = generate_id(
            f"{dict_other_user.ip}:{dict_other_user.port}", capacity)
        url = server_other_user.get_ip_port(nickname_user, -1)

        requests.post('http://'+url+'/ReceiveMessage', params={
                      "nickname_from": my_nickname, "nickname_to": nickname_user, 'value': message})
    except:
        # buscar el entity en que está almacenada la información del usuario
        # dict_node_data = node_data.nickname_entity_node(my_nickname)
        # if dict_node_data is None:
        #     return "Your data has been lost"

        # si la informacion de los usuarios no se guarda en la misma base datos, gurdarlo en la de el tambien
        # if dict_other_user['ip'] != dict_node_data['ip'] or dict_other_user['port'] != dict_node_data['port']:
        # si su servidor está activo y no es mi mismo servidor hago lo mismo.
        if add_messenge(dict_other_user, my_nickname, nickname_user, message) is False:
            return 'send failed'
        # si mi server está activo le mando el mensaje para ser escrito y replico los datos
        # if replication_messenge(dict_node_data, client.user, user, message) is False:
        #     return 'send failed'
    client.add_messenges(my_nickname, nickname_user, message, -1)
    return


@service.post("/ReceiveMessage")
def receive_message(nickname_from: str, nickname_to: str, value: str):
    client.add_messenges(nickname_from, nickname_to, value, -1)


@client_interface.get("/GetContacts")
def get_contacts():
    if not client.login:
        return "You are not logged in"
    result = {}
    contacts = client.get_contacts()
    for contact in contacts:
        result[contact[1]] = contact[0]
    return result


@client_interface.post("/AddContacts")
def add_contacts(name: str, nickname: str):
    if not client.login:
        return "You are not logged in"
    client.add_contacts(nickname, name)


@client_interface.post("/DeleteContacts")
def delete_contacts(name: str):
    if not client.login:
        return "You are not logged in"
    client.delete_contact(name)
    pass


@client_interface.get("/GetChats")
def get_chats():
    if not client.login:
        return "You are not logged in"
    result = []
    contacts_nickname = []
    contacts_name = []
    # mynickname = client.user['nickname']

    # contacts = client.get_contacts()
    # for contact in contacts:
    #    contacts_nickname.append(contact[0])
    #    contacts_name.append(contact[1])

    chats = client.get_chats()
    for chat in chats:
        name = client.get_name(chat)
        if name is not None:
            result.append(name)
        else:
            result.append(chat)
        # try:
        #     i = contacts_nickname.index(chat)
        #     result.append(contacts_name[i])
        # except:
        #     result.append(chat)

    return result
