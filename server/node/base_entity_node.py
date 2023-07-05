from ..chord.base_node import BaseNode

class BaseEntityNode:
    def add_user(self, nickname: str, pasword: str, database_original: bool) -> bool:
        raise NotImplementedError()
    
    def get_pasword(self, nickname: str, database_original: bool) -> str:
        raise NotImplementedError()
    
    def nickname_entity_node(self, nickname: str, database_original: bool) -> "BaseEntityNode":
        raise NotImplementedError()
    
    def search_entity_node(self, nickname: str) -> BaseNode:
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
    
    def add_chat(self, user_id_1_: str, user_id_2_: str, database_original: bool) -> bool:
        raise NotImplementedError()
    
    def search_chat_id(self, user_id_1: str, user_id_2: str, database_original: bool) -> int:
        raise NotImplementedError()
    
    def delete_chat(self, user_id_1: str, user_id_2: str, database_original: bool) -> bool:
        raise NotImplementedError()
    
    def search_chat(self, user_id_1: str, user_id_2: str, database_original: bool) -> list:
        raise NotImplementedError()
    
    def fingers_predecessor_list(self) -> list[tuple[str, str]]:
        raise NotImplementedError()