from typing import Union

from data.database_entity import DataBaseUser
from ..chord.base_node import BaseNode


class BaseEntityNode(BaseNode):
    # region RETURN TYPE OVERLOAD
    def successor(self) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    def predecessor(self) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    def find_successor(self, id: int) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()
    # endregion

    def get_users(self, database_id: int = -1) -> list[tuple[str,str,str,str]]:
        raise NotImplementedError()

    def add_user(self, nickname: str, pasword: str, ip: str, port: str, database_id: int = -1) -> bool:
        raise NotImplementedError()

    def get_pasword(self, nickname: str, database_id: int = -1) -> str:
        raise NotImplementedError()

    def delete_user(self, nickname: str, database_id: int = -1) -> bool:
        raise NotImplementedError()

    def update_user(self, nickname: str, ip: str, port: str, database_id: int = -1) -> bool:
        raise NotImplementedError()

    def get_ip_port(self, nickname: str, database_id: int = -1) -> str:
        raise NotImplementedError()

    def nickname_entity_node(self, nickname: str, database_id: int = -1) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    def search_entity_node(self, nickname: str) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()
    
    def get_messages(self)-> list[tuple[int,str,str,str]]:
        raise NotImplementedError()
    
    def add_messenger(self, source: str, destiny: str, value: str, database_id: int = -1) -> bool:
        raise NotImplementedError()

    def delete_messenges(self, id_messenger: int, database_id: int = -1) -> bool:
        raise NotImplementedError()
    
    def search_messenger_from(self, me: str, user: str, database_id: int = -1) -> list[tuple[str,str]]:
        raise NotImplementedError()

    def search_messenger_to(self, me: str, user: str, database_id: int = -1) -> list[tuple[str,str]]:
        raise NotImplementedError()

    def delete_messenges_from(self,me:str, user:str = '')-> bool:
        raise NotImplementedError()
        
    def delete_messenges_to(self,me:str,user:str=' ')-> bool:
        raise NotImplementedError()
        
    def database_serialize(self, database_id: int = -1) -> dict:
        raise NotImplementedError()

    def copy_database(self, source: DataBaseUser, database_id: int = -1) -> None:
        raise NotImplementedError()
