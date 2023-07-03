from requests import get, put, delete

from ..chord.remote_node import RemoteNode as ChordRemoteNode
from ..chord.base_node import BaseNodeModel


class RemoteEntityNode(ChordRemoteNode):

    def add_user(self, nickname: str, pasword: str):
        response = put(f"{self.url}/user/add", data = {"nickname": nickname, "pasword": pasword})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])
    
    def nickname_entity_node(self, nickname):
        response = get(f"{self.url}/info/entity/{nickname}")

        if response.status_code == 200:
            result: dict = response.json()
            return result
        
        raise Exception(response.json()["detail"])

    def delete_user(self, nickname: str):
        response = delete(f"{self.url}/user/delete/{nickname}")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def add_messenger(self, source, destiny, value):
        response = put(f"{self.url}/messenger/add", data = {"source": source, "destiny":destiny, "value": value})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def delete_messenger(self, nickname: str):
        response = delete(f"{self.url}/messenger/delete/{nickname}")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_messenger_from(self, me, user):
        response = get(f"{self.url}/messenger/from", data = {"me": me, "user": user})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_messenger_to(self, me, user):
        response = get(f"{self.url}/messenger/to", data = {"me": me, "user": user})

        if response.status_code == 200:
            result: list = response.json()
            return result

        raise Exception(response.json()["detail"])

    def add_chat(self, user_id_1, user_id_2):
        response = put(f"{self.url}/chat/add", data = {"user_id_1": user_id_1, "user_id_2": user_id_2})

        if response.status_code == 200:
            result: list = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_chat_id(self, user_id_1, user_id_2):
        response = get(f"{self.url}/chat", data = {"user_id_1": user_id_1, "user_id_2": user_id_2})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def delete_chat(self, user_1, user_2):
        response = delete(f"{self.url}/chat/delete/{user_1}/{user_2}")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])
    
    def fingers_predecessor_list(self):
        response = get(f"{self.url}/info/fingers_predecessor")

        if response.status_code == 200:
            result: list = response.json()
            return result
        
        raise Exception(response.json()["detail"])
    