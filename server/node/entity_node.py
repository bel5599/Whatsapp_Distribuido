from ..chord.node import Node as ChordNode
from ...data.function_db import *


class EntityNode(ChordNode):
    def __init__(self, id: int, ip: str, port: str):
        super().__init__(id, ip, port)
        create_database()

    def add_user(self, nickname: str, password: str):
        return add_user(nickname, password)
    
    def nickname_entity_node(self, nickname):
        if contain_user(nickname): return self
        self.successor.nickname_entity_node(nickname)

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
