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
                result: list = response.json()["users"]
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

    def add_messenges(self, source: str, destiny: str, value: str, database_id: int):
        try:
            response = self._manager.put("/messenges/add",
                                         data={"source": source, "destiny": destiny, "value": value, "database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: bool = response.json()["success"]
                return result

            print("ERROR:", response.json()["detail"])

        return False

    def delete_messenges(self, id: int, database_id: int):
        try:
            response = self._manager.delete(
                f"/messenges/delete/{id}", data={"database_original": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: bool = response.json()["success"]
                return result

            print("ERROR:", response.json()["detail"])

        return False

    def search_messenges_from(self, me: str, user: str, database_id: int):
        try:
            response = self._manager.get("/messenges/from",
                                         data={"me": me, "user": user, "database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: list = response.json()
                return result

            print("ERROR:", response.json()["detail"])

        return []

    def search_messenges_to(self, me: str, user: str, database_id: int):
        try:
            response = self._manager.get("/messenges/to",
                                         data={"me": me, "user": user, "database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: list = response.json()
                return result

            print("ERROR:", response.json()["detail"])

        return []

    def get_messages(self, database_id: int):
        try:
            response = self._manager.get("/messenges",
                                         data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: list = response.json()
                return result

            print("ERROR:", response.json()["detail"])

        return []

    def delete_messenges_to(self, me: str, database_id: int):
        try:
            response = self._manager.delete(f"/messenges/to/{me}",
                                            data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: bool = response.json()["success"]
                return result

            print("ERROR:", response.json()["detail"])

        return False

    def delete_messenges_from(self, me: str, database_id: int):
        try:
            response = self._manager.delete(f"/messenges/from/{me}",
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

    def database_serialize(self, database_id: int):
        # FIXME: falta el handler de esta ruta
        try:
            response = self._manager.get(
                "/info/database_serialize", data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: dict = response.json()
                return result

            print("ERROR:", response.json()["detail"])

    def copy_database(self, source: DataBaseUserModel, database_id: int):
        try:
            response = self._manager.get(
                "/info/copy_database", data={"source": source, "database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                result: dict = response.json()
                return result

            print("ERROR:", response.json()["detail"])

    # endregion
