from pydantic import BaseModel

from ..chord.node import Node as ChordNode
from ...data.function_db import *
from ..util import generate_id


class ChatModel(BaseModel):
    user_1: str
    user_2: str


class MessengerModel(BaseModel):
    source: str
    destiny: str
    value: str


class UserModel(BaseModel):
    nickname: str
    password: str


class EntityNode(ChordNode):
    def __init__(self, ip: str, port: str, capacity: int):
        super().__init__(ip, port, capacity)
        create_database()

    def add_user(self, nickname: str, password: str):
        return add_user(nickname, password)

    def nickname_entity_node(self, nickname: str):
        if contain_user(nickname):
            return self

        return self.successor.nickname_entity_node_rec(nickname, self)

    def nickname_entity_node_rec(self, nickname: str, node):
        if self.id == node.id:
            return None

        if contain_user(nickname):
            return self
        return self.successor.nickname_entity_node_rec(nickname, node)
    
    def search_node(self):
        id = generate_id(f"{self.ip}:{self.port}", self.network_capacity())
        
        if id >= self.id:
            return self
        
        node = self.successor
        while(not self.id == node.id):
            if id >= node.id:
                return node
            else:
                node.successor()


    def delete_user(self, nickname):
        return delete_user(nickname)

    def add_messenger(self, source, destiny, value):
        return add_messenger(source, destiny, value)

    def search_messenger_from(self, me, user):
        return search_messenger_from(me, user)

    def search_messenger_to(self, me, user):
        return search_messenger_to(me, user)

    def delete_messenger(self, id_messenger):
        return delete_messenger(id_messenger)

    def add_chat(self, user_id_1_, user_id_2_):
        return add_chat(user_id_1_, user_id_2_)

    def search_chat_id(self, user_id_1, user_id_2):
        return search_chat_id(user_id_1, user_id_2)

    def delete_chat(self, user_id_1, user_id_2):
        return delete_chat(user_id_1, user_id_2)

    def fingers_predecessor_list(self):
        fingers_list = [(finger.node.ip, finger.node.port)
                        for finger in self.fingers if finger.node is not None]
        if not self._predecessor == None:
            fingers_list.append((self._predecessor.ip, self._predecessor.port))

        return fingers_list
    
    def get_pasword(self, nickname):
        return get_password(nickname)
