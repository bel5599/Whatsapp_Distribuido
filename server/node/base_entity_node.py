from typing import Union

from data.database_entity import DataBaseUser
from ..chord.base_node import BaseNode
from .models import DataBaseUserModel


class BaseEntityNode(BaseNode):
    # region RETURN TYPE OVERLOAD
    def successor(self) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    def predecessor(self) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    def find_successor(self, id: int) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()
    # endregion

    # region USER
    def get_users(self, database_id: int = -1) -> list[tuple[str, str, str, str]]:
        raise NotImplementedError()

    def add_user(self, nickname: str, pasword: str, ip: str, port: str, database_id: int) -> bool:
        raise NotImplementedError()

    def get_pasword(self, nickname: str, database_id: int) -> str:
        raise NotImplementedError()

    def delete_user(self, nickname: str, database_id: int) -> bool:
        raise NotImplementedError()

    def update_user(self, nickname: str, ip: str, port: str, database_id: int) -> bool:
        raise NotImplementedError()

    def get_ip_port(self, nickname: str, database_id: int) -> str:
        raise NotImplementedError()

    def nickname_entity_node(self, nickname: str, search_id: int, database_id: int) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    def search_entity_node(self, nickname: str) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()
    # endregion

    # region MESSAGES
    def add_messages(self, source: str, destiny: str, value: str, database_id: int) -> bool:
        raise NotImplementedError()

    def search_messages_to(self, me: str, user: str, database_id: int) -> list[tuple[str, str]]:
        raise NotImplementedError()

    def delete_messages_to(self, me: str, database_id: int) -> bool:
        raise NotImplementedError()

    # def delete_messages(self, id_messenger: int, database_id: int) -> bool:
    #     raise NotImplementedError()

    # def search_messages_from(self, me: str, user: str, database_id: int) -> list[tuple[str, str]]:
    #     raise NotImplementedError()

    # def get_messages(self, database_id: int) -> list:
    #     raise NotImplementedError()

    # def delete_messages_from(self, me: str, database_id: int) -> bool:
    #     raise NotImplementedError()
    # endregion

    # region REPLICATION
    def replicate(self, data: DataBaseUserModel, database_id: int) -> None:
        raise NotImplementedError()
    # endregion
