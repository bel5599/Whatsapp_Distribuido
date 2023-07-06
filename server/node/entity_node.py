from pydantic import BaseModel

from ..chord.node import Node as ChordNode
from data.database_entity import DataBaseUser
from ..util import generate_id


class MessengerModel(BaseModel):
    source: str
    destiny: str
    value: str
    database_original: bool


class UserModel(BaseModel):
    nickname: str
    password: str
    ip: str
    port: str
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
        self.database = DataBaseUser("data")
        self.replication_database = DataBaseUser("replication_data")

    # User
    # Arreglar
    def add_user(self, nickname: str, password: str, ip: str, port: str, database_original):
        if database_original:
            return self.database.add_user(nickname, password)
        return self.replication_database.add_user(nickname, password)

    def get_users(self, database_original: bool):
        if database_original:
            return self.database.get_users()

    def get_pasword(self, nickname: str, database_original: bool):
        if database_original:
            return self.database.get_password(nickname)
        return self.replication_database.get_password(nickname)

    def delete_user(self, nickname: str, database_original: bool):
        if database_original:
            return self.database.delete_user(nickname)
        return self.replication_database.delete_user(nickname)

    def update_user(self, nickanme: str, ip: str, port: str, database_original: bool):
        if database_original:
            return self.database.update_user(nickanme, ip, port)
        return self.replication_database.update_user(nickanme, ip, port)

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

    # MESSENGES

    def add_messenges(self, source: str, destiny: str, value: str, database_original: bool):
        if database_original:
            return self.database.add_messenges(source, destiny, value)
        return self.replication_database.add_messenges(source, destiny, value)

    def search_messenges_from(self, me: str, user: str, database_original: bool):
        if database_original:
            return self.database.search_messenges_from(me, user)
        return self.replication_database.search_messenges_from(me, user)

    def search_messenges_to(self, me: str, user: str, database_original: bool):
        if database_original:
            return self.database.search_messenges_to(me, user)
        return self.replication_database.search_messenges_to(me, user)

    def delete_messenges(self, id_messenger: int, database_original: bool):
        if database_original:
            return self.database.delete_messenges(id_messenger)
        return self.replication_database.delete_messenges(id_messenger)
