from typing import Any

from ..chord.remote_node import RemoteNode as ChordRemoteNode
from ..chord.base_node import BaseNodeModel
from .base_entity_node import BaseEntityNode
from .models import DataBaseUserModel


class RemoteEntityNode(ChordRemoteNode, BaseEntityNode):
    # region RETURN TYPE OVERLOAD
    def _ensure_local(self, node: ChordRemoteNode) -> BaseEntityNode:
        result_node: Any = super()._ensure_local(node)
        return result_node
    # endregion

    # region USER

    def get_users(self, database_id: int = -1):
        try:
            response = self._manager.get(
                "/info/users", data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: list = response.json()
                return result

            print("ERROR:", response.json()["detail"])

        return []

    def add_user(self, nickname: str, pasword: str,  ip: str, port: str, database_id: int):
        try:
            response = self._manager.put(
                "/user/add", data={"nickname": nickname, "pasword": pasword, "ip": ip, "port": port, "database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: bool = response.json()["success"]
                return result

            print("ERROR:", response.json()["detail"])

        return False

    def get_pasword(self, nickname: str, database_id: int):
        try:
            response = self._manager.get(
                f"/user/pasword/{nickname}", data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: str = response.json()["pasword"]
                return result

            print("ERROR:", response.json()["detail"])

        return ""

    def delete_user(self, nickname: str, database_id: int):
        try:
            response = self._manager.delete(
                f"/user/delete/{nickname}", data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: bool = response.json()["success"]
                return result

            print("ERROR:", response.json()["detail"])

        return False

    def update_user(self, nickname: str, ip: str, port: str, database_id: int):
        try:
            response = self._manager.put(
                "/user/update", data={'nickname': nickname, "ip": ip, "port": port, "database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: bool = response.json()["success"]
                return result

            print("ERROR:", response.json()["detail"])

        return False

    def get_ip_port(self, nickname: str, database_id: int):
        try:
            response = self._manager.get(
                f"/user/ip_port/{nickname}", data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: str = response.json()["ip_port"]
                return result

            print("ERROR:", response.json()["detail"])

        return ""

    def nickname_entity_node(self, nickname: str, database_id: int):
        try:
            response = self._manager.get(
                f"/info/entity/{nickname}", data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return self._ensure_local(self.__class__.from_base_model(model))

            print("ERROR:", response.json()["detail"])

    def search_entity_node(self, nickname: str):
        try:
            response = self._manager.get(f"/info/search_entity/{nickname}")
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return self._ensure_local(self.__class__.from_base_model(model))

            print("ERROR:", response.json()["detail"])

    # endregion

    # region MESSAGES

    def add_messages(self, source: str, destiny: str, value: str, database_id: int):
        try:
            response = self._manager.put("/messages/add",
                                         data={"source": source, "destiny": destiny, "value": value, "database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: bool = response.json()["success"]
                return result

            print("ERROR:", response.json()["detail"])

        return False

    def search_messages_to(self, me: str, user: str, database_id: int):
        try:
            response = self._manager.get("/messages/to",
                                         data={"me": me, "user": user, "database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: list = response.json()
                return result

            print("ERROR:", response.json()["detail"])

        return []

    def delete_messages_to(self, me: str, database_id: int):
        try:
            response = self._manager.delete(f"/messages/to/{me}",
                                            data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: bool = response.json()["success"]
                return result

            print("ERROR:", response.json()["detail"])

        return False

    # endregion

    # region REPLICATION

    def replicate(self, data: DataBaseUserModel, database_id: int):
        body = {
            "source": data.serialize(),
            "database_id": database_id
        }

        try:
            response = self._manager.put("/info/replicate", data=body)
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code != 200:
                print("ERROR:", response.json()["detail"])

    # endregion
