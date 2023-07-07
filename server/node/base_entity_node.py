from typing import Union

from ..chord.base_node import BaseNode
from ...data.database_entity import DataBaseUser


class BaseEntityNode(BaseNode):
    def add_user(self, nickname: str, pasword: str, ip: str, port: str, database_original: bool) -> bool:
        raise NotImplementedError()

    def get_pasword(self, nickname: str, database_original: bool) -> str:
        raise NotImplementedError()

    def nickname_entity_node(self, nickname: str, database_original: bool) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    def search_entity_node(self, nickname: str) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    def delete_user(self, nickname: str, database_original: bool) -> bool:
        raise NotImplementedError()

    def add_messenger(self, source: str, destiny: str, value: str, database_original: bool) -> bool:
        raise NotImplementedError()

    def search_messenger_from(self, me: str, user: str, database_original: bool) -> list:
        raise NotImplementedError()

    def search_messenger_to(self, me: str, user: str, database_original: bool) -> list:
        raise NotImplementedError()

    def delete_messenger(self, id_messenger: int, database_original: bool) -> bool:
        raise NotImplementedError()

    def copy_database(self, source: DataBaseUser, database_id: int) -> None:
        raise NotImplementedError()