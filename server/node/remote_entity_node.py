from requests import get, put, delete

from ..chord.remote_node import RemoteNode as ChordRemoteNode
from ..chord.base_node import BaseNodeModel


class RemoteEntityNode(ChordRemoteNode):

    def add_user(self):
        response = put(f"{self.url}/user/add")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])
    
    def nickname_entity_node(self, nickname):
        response = get(f"{self.url}/user/entity{nickname}")

        if response.status_code == 200:
            model = BaseNodeModel(**response.json())
            return RemoteEntityNode.from_base_model(model)
        
        raise Exception(response.json()["detail"])

    def delete_user(self, nickname: str):
        response = delete(f"{self.url}/user/delete/{nickname}")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def add_messenger(self):
        response = put(f"{self.url}/messenger/add")

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

    def search_messenger_from(self):
        response = get(f"{self.url}/messenger/from")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_messenger_to(self):
        response = get(f"{self.url}/messenger/to")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def add_chat(self):
        response = put(f"{self.url}/chat/add")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_chat_id(self):
        response = get(f"{self.url}/chat")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def delete_chat(self, user_1, user_2):
        response = delete(f"{self.url}/chat/delete/{user_1}{user_2}")

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])