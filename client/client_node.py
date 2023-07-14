import json
from service.heartbeat import HeartBeatManager
from service.requests import RequestManager
from data.database_client import DataBaseClient
from shared import get_ip
from .utils import FIXED_PORT


class ClientNode:
    def __init__(self):
        self.user = {}
        self.login = False
        self.manager = HeartBeatManager()
        self.ip = get_ip()
        self.port = FIXED_PORT
        self.database = DataBaseClient()

    def login_user(self, nickname: str, password: str):
        self.user['nickname'] = nickname
        self.user['password'] = password
        self.login = True
        
    def add_servers(self,servers:list):
        for s in servers:
            ip, port = s.split(':')
            self.manager.add_request_manager(RequestManager(ip, port))
    
    def server_list(self):
        return list(self.manager.request_manager_list)

    def logout_user(self):
        self.user = {}
        self.manager = HeartBeatManager()
        self.login = False

    def update_servers(self):
        self.manager.check_health()

    def save_ip_port(self, ip_port_list: list):
        ip = self.ip[::-1]
        ip_ = ip.split(".", 1)
        ip = ip_[1][::-1]

        data = {"ip": ip, "port":self.port}
        ip_port_list.append(data)
        self.save_infor("server_addresses_cache.json", data)

    def save_infor(self, file_name, data: list):
        with open(file_name, "w") as j:
            json.dumps(data, j)

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
