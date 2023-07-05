from pydantic import BaseModel

from ..chord.node import Node as ChordNode
from ...data.database import DataBase
from ..util import generate_id


class MessengerModel(BaseModel):
    source: str
    destiny: str
    value: str
    database_original: bool


class UserModel(BaseModel):
    nickname: str
    password: str
    database_original: bool


class ChatModel(BaseModel):
    user_id_1: str
    user_id_2: str
    database_original: bool


class DataBaseModel(BaseModel):
    database_original: bool


class SearchMessengerModel(BaseModel):
    source: str
    destiny: str
    database_original: bool


class EntityNode(ChordNode):
    def __init__(self, ip: str, port: str, capacity: int):
        super().__init__(ip, port, capacity)
        self.database = DataBase("data")
        self.replication_database = DataBase("replication_data")

    def add_user(self, nickname: str, password: str, database_original):
        if database_original:
            return self.database.add_user(nickname, password)
        return self.replication_database.add_user(nickname, password)
    
    def get_pasword(self, nickname: str, database_original: bool):
        if database_original:
            return self.database.get_password(nickname)
        return self.replication_database.get_password(nickname)

    def nickname_entity_node(self, nickname: str, database_original: bool):
        if database_original:
            self.database.contain_user(nickname)
            return self
        if self.database.contain_user(nickname) or self.replication_database.contain_user(nickname):
            return self

        return self.successor.nickname_entity_node_rec(nickname, self, database_original)

    def nickname_entity_node_rec(self, nickname: str, node, database_original: bool):
        if self.id == node.id:
            return None

        if database_original:
            self.database.contain_user(nickname)
            return self
        if self.database.contain_user(nickname) or self.replication_database.contain_user(nickname):
            return self
        return self.successor.nickname_entity_node_rec(nickname, node, database_original)
    
    def search_entity_node(self, nickname: str):
        id = generate_id(nickname, self.network_capacity())
        return self.find_successor(id)

    def delete_user(self, nickname: str, database_original: bool):
        if database_original:
            return self.database.delete_user(nickname)
        return self.replication_database.delete_user(nickname)

    def add_messenger(self, source: str, destiny: str, value: str, database_original: bool):
        if database_original:
            return self.database.add_messenger(source, destiny, value)
        return self.replication_database.add_messenger(source, destiny, value)

    def search_messenger_from(self, me: str, user: str, database_original: bool):
        if database_original:
            return self.database.search_messenger_from(me, user)
        return self.replication_database.search_messenger_from(me, user)

    def search_messenger_to(self, me: str, user: str, database_original: bool):
        if database_original:
            return self.database.search_messenger_to(me, user)
        return self.replication_database.search_messenger_to(me, user)

    def delete_messenger(self, id_messenger: int, database_original: bool):
        if database_original:
            return self.database.delete_messenger(id_messenger)
        return self.replication_database.delete_messenger(id_messenger)

    def add_chat(self, user_id_1_: str, user_id_2_: str, database_original: bool):
        if database_original:
            return self.database.add_chat(user_id_1_, user_id_2_)
        return self.replication_database.add_chat(user_id_1_, user_id_2_)

    def search_chat_id(self, user_id_1: str, user_id_2: str, database_original: bool):
        if database_original:
            return self.database.search_chat_id(user_id_1, user_id_2)
        return self.replication_database.search_chat_id(user_id_1, user_id_2)

    def delete_chat(self, user_id_1: str, user_id_2: str, database_original: bool):
        if database_original:
            return self.database.delete_chat(user_id_1, user_id_2)
        return self.replication_database.delete_chat(user_id_1, user_id_2)

    def fingers_predecessor_list(self):
        fingers_list = [(finger.node.ip, finger.node.port)
                        for finger in self.fingers if finger.node is not None]
        if not self._predecessor == None:
            fingers_list.append((self._predecessor.ip, self._predecessor.port))

        return fingers_list

    def search_chat(self, user_id_1: str, user_id_2: str, database_original: bool):
        if database_original:
            return self.database.search_chat(user_id_1, user_id_2)
        return self.replication_database.search_chat(user_id_1, user_id_2)
