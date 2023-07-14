import json

from service.heartbeat import HeartBeatManager
from data.database_client import DataBaseClient
from shared import get_ip, CLIENT_PORT
from .utils import SERVER_ADDRESSES_CACHE_FILENAME


class ClientNode:
    def __init__(self):
        self.user = {}
        self.login = False
        self.manager = HeartBeatManager()
        self.ip = get_ip()
        self.port = CLIENT_PORT
        self.database = DataBaseClient()

    def login_user(self, nickname: str, password: str):
        self.user['nickname'] = nickname
        self.user['password'] = password
        self.login = True

    def logout_user(self):
        self.user = {}
        self.manager = HeartBeatManager()
        self.login = False

    def update_servers(self):
        self.manager.check_health()

    def save_nodes(self):
        nodes = [node.serialize() for node in self.manager.get_nodes()]
        self.save_info(SERVER_ADDRESSES_CACHE_FILENAME, nodes)

    def save_info(self, file_name, data: list):
        with open(file_name, "w") as j:
            json.dump(data, j)

    # Aqui van los metodos de la base datos desde el cliente

    # Contacts
    def get_contacts(self):
        return [(nickname, name) for (nickname, name) in self.database.get_contacts(self.user['nickname'])]

    def add_contacts(self, nickname: str, name: str):
        return self.database.add_contacts(self.user['nickname'], nickname, name)

    def update_contact(self, nickname: str, name: str):
        return self.database.update_contact(self.user['nickname'], nickname, name)

    def contain_contact(self, nickname: str):
        return self.database.contain_contact(self.user['nickname'], nickname)

    def delete_contact(self, nickname: str):
        return self.database.delete_contact(self.user['nickname'], nickname)

    def get_name(self, nickname: str):
        return self.database.get_name(self.user['nickname'], nickname)

    def get_nickname(self, name: str):
        return self.database.get_nickname(self.user['nickname'], name)

    # MESSAGES
    def get_messages(self):
        return self.database.get_messages()

    def add_messenges(self, source: str, destiny: str, value: str, id: int = -1):
        return self.database.add_messages(source, destiny, value, id)

    def delete_messenges(self, id_messenge: int):
        return self.database.delete_messages(id_messenge)

    def search_messenges_from(self, me: str, user: str):
        return self.database.search_messages_from(me, user)

    def search_messenges_to(self, me: str, user: str):
        return self.database.search_messages_to(me, user)

    # CHAT
    def get_chats(self):
        return self.database.get_chats(self.user['nickname'])

    def add_chat(self, user_id_1_: str, user_id_2_: str):
        return self.database.add_chat(user_id_1_, user_id_2_)

    def search_chat_id(self, user_id_1: str, user_id_2: str):
        return self.database.search_chat_id(user_id_1, user_id_2)

    def delete_chat(self, user_id_1: str, user_id_2: str):
        return self.database.delete_chat(user_id_1, user_id_2)

    def search_chat(self, user_id_2: str):
        return self.database.search_chat(self.user['nickname'], user_id_2)
