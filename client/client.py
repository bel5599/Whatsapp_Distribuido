from fastapi import FastAPI
import json
import requests
from fastapi_utils.tasks import repeat_every
from sqlalchemy import true
import os
from client_node import ClientNode

client_interface = FastAPI()
client = ClientNode()


@client_interface.post("/Register")
def register(nickname: str, password: str, server: str):
    # url = 'http://'+server+ nombredelmetodoquebuscaelentity
    # Hashear el nickname para obtener un servidor
    # Registrar los datos del usuario
    # Loguear al usuario

    # Ver como seria la conexion
    # requests.post('http://'+server+'/RegisterUser', params= {"name": name, "nickname": nickname, "password": password})
    return


@client_interface.post("/Login")
def login(nickname: str, password: str):
    # Hashear el nickname para obtener un servidor
    # Verificar que el servidor este activo
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
