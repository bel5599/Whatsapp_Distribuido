from typing import Union

from ..chord.base_node import BaseNode
from ...data.database_entity import DataBaseUser


class BaseEntityNode(BaseNode):
    
    def get_users(self,database_id: int=-1) -> Union[list,bool]:
        raise NotImplementedError()
    
    def add_user(self, nickname: str, pasword: str, ip: str, port: str, database_id: int=-1) -> bool:
        raise NotImplementedError()
    
    def get_pasword(self, nickname: str, database_id: int=-1) -> str:
        raise NotImplementedError()

    def delete_user(self, nickname: str, database_id: int=-1) -> bool:
        raise NotImplementedError()
    
    def update_user(self,nickname:str,ip:str,port:str,database_id: int=-1)-> bool:
        raise NotImplementedError()
        
    def get_ip_port(self,nickname:str,database_id: int=-1)-> str:
        raise NotImplementedError()
    
    
    def nickname_entity_node(self, nickname: str, database_id: int=-1) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    def search_entity_node(self, nickname: str) -> Union["BaseEntityNode", None]:
        raise NotImplementedError()

    
    def add_messenger(self, source: str, destiny: str, value: str, database_id: int=-1) -> bool:
        raise NotImplementedError()

    def search_messenger_from(self, me: str, user: str, database_id: int=-1) -> list:
        raise NotImplementedError()

    def search_messenger_to(self, me: str, user: str, database_id: int=-1) -> list:
        raise NotImplementedError()

    def delete_messenger(self, id_messenger: int, database_id: int=-1) -> bool:
        raise NotImplementedError()
    
    def database_serialize(self,database_id: int = -1)-> dict:
        raise NotImplementedError()
    
    def copy_database(self, source: DataBaseUser, database_id: int=-1) -> None:
        raise NotImplementedError()