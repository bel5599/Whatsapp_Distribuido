from typing import Union
from fastapi import FastAPI

from server.node.remote_entity_node import RemoteEntityNode
from server.util import generate_id
from service.requests import RequestManager
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

    # Busca el posible nodo a guardar los datos de usuario
    try:
        node = server_node.search_entity_node(nickname)
    except:
        return "Wrong server"

    node_data: Union[BaseEntityNode, None] = None

    if node is not None:
        node_data = node.nickname_entity_node(nickname, -1)
        # verificar si el usuario ya esta en el sistema y validacion del servidor de entrada
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

        servers.append(server)
        servers.append(node_data.ip+":"+node_data.port)
    # Loguear al usuario
    client.login_user(nickname, password, servers)
    return 'Register Successful'


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

    # Busca el posible nodo a guardar los datos de usuario
    try:
        node = server_node.search_entity_node(nickname)
    except:
        return "Wrong server"

    node_data: Union[BaseEntityNode, None] = None
    # verificar si el usuario ya esta en el sistema y validacion del servidor de entrada
    try:
        if node is not None:
            node_data = node.nickname_entity_node(nickname, -1)
            if node_data is None:
                return "You are not registered"
    except:
        return "Login failed"

    # verificar que no se ha caido el servidor
    if node_data is not None:
        try:
            # Verificar contrasenna y retornar una notificacion
            password_server = node_data.get_pasword(nickname, -1)
            if password_server is not None and password != password_server:
                return "Wrong password"

            # Si cambio el ip y el port actualizar estos valores y actualizar en los sucessores
            node_data.update_user(nickname, client.ip, client.port, -1)

            # Agrega al entity que guarda los datos del cliente, sucesor, sucesor del sucesor y por el q se conecta
            servers = []
            servers.append(server)
            servers.append(node_data.ip+":"+node_data.port)

            # Loguear al usuario
            client.login_user(nickname, password, servers)

            # Recivo los sms que tenia en espera
            task_receive_message(client.user['nickname'], client.database,
                                 node_data)
            return 'Login Successful'
        except Exception as e:
            return "Login failed"

# FALTA


@client_interface.post("/Logout")
def logout():
    client.logout_user()
    return 'Logout Successful'


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

    request_manager = servers[0]
    ip = request_manager.ip
    port = request_manager.port

    try:
        node_data = RemoteEntityNode(-1, ip, port)
        capacity = node_data.network_capacity()
        node_data.id = generate_id(f"{ip}:{port}", capacity)

    except:
        return 'Broken Connection, you need to logout and login again'

    # buscar el entity en que está almacenada la información del otro usuario
    dict_other_user = node_data.nickname_entity_node(nickname_user, -1)
    if dict_other_user is None:
        return user+"is not register"

    my_nickname = client.user['nickname']

    try:
        ip, port = dict_other_user.get_ip_port(nickname_user, -1).split(":")
        rm = RequestManager(ip, port)
        rm.post("/ReceiveMessage", params={
            "nickname_from": my_nickname, "nickname_to": nickname_user, 'value': message})
    except:
        if add_messenge(dict_other_user, my_nickname, nickname_user, message) is False:
            return 'send failed'

    client.add_messenges(my_nickname, nickname_user, message, -1)
    return "Send Message"


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

    # VERIFICAR QUE LOS SERVIDORES ESTEN ACTIVOS Y ACTUALIZAR LA LISTA DE SERVERS DEL USUARIO
    servers = client.server_list()

    # server que contiene informacion
    if len(servers) == 0:
        return 'Broken Connection, you need to exit the login and login again'

    request_manager = servers[0]
    ip = request_manager.ip
    port = request_manager.port

    try:
        node_data = RemoteEntityNode(-1, ip, port)
        capacity = node_data.network_capacity()
        node_data.id = generate_id(f"{ip}:{port}", capacity)
    except:
        return 'Broken Connection, you need to exit the login and login again'

    dict_other_user = node_data.nickname_entity_node(nickname, -1)
    if dict_other_user is None:
        return nickname+"is not register"

    client.add_contacts(nickname, name)
    return 'Add Contacts Successful'


@client_interface.post("/DeleteContacts")
def delete_contacts(name: str):
    if not client.login:
        return "You are not logged in"
    client.delete_contact(name)
    return 'Delete Contacts Successful'


@client_interface.get("/GetChats")
def get_chats():
    if not client.login:
        return "You are not logged in"

    result = []
    chats = client.get_chats()
    for chat in chats:
        name = client.get_name(chat)
        if name is not None:
            result.append(name)
        else:
            result.append(chat)
    return result
