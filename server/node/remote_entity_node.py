from typing import Any

from ..chord.remote_node import RemoteNode as ChordRemoteNode
from ..chord.base_node import BaseNodeModel
from .base_entity_node import BaseEntityNode
from ...data.database_entity import DataBaseUser

from .entity_node import DataBaseUserModel


class RemoteEntityNode(ChordRemoteNode, BaseEntityNode):
    # region RETURN TYPE OVERLOAD
    def _ensure_local(self, node: ChordRemoteNode) -> BaseEntityNode:
        result_node: Any = super()._ensure_local(node)
        return result_node
    # endregion

    # User
    def add_user(self, nickname: str, pasword: str,  ip: str, port: str, database_id: int = -1):
        response = self._manager.put(
            "/user/add", data={"nickname": nickname, "pasword": pasword, "ip": ip, "port": port, "database_id": database_id})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def get_pasword(self, nickname: str, database_id: int = -1):
        response = self._manager.get(
            f"/user/pasword/{nickname}", data={"database_id": database_id})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def delete_user(self, nickname: str, database_id: int = -1):
        response = self._manager.delete(
            f"/user/delete/{nickname}", data={"database_id": database_id})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def nickname_entity_node(self, nickname: str, database_id: int = -1):
        try:
            response = self._manager.get(
                f"/info/entity/{nickname}", data={"database_id": database_id})
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return self._ensure_local(RemoteEntityNode.from_base_model(model))

            print("ERROR:", response.json()["detail"])

    def search_entity_node(self, nickname: str = -1):
        try:
            response = self._manager.get(f"/info/search_entity/{nickname}")
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return self._ensure_local(RemoteEntityNode.from_base_model(model))

            print("ERROR:", response.json()["detail"])

    # MESSENGES

    def add_messenges(self, source: str, destiny: str, value: str, database_id: int = -1):
        response = self._manager.put("/messenger/add",
                                     data={"source": source, "destiny": destiny, "value": value, "database_id": database_id})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def delete_messenges(self, id: int, database_id: int = -1):
        response = self._manager.delete(
            f"/messenger/delete/{id}", data={"database_original": database_id})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_messenges_from(self, me: str, user: str, database_id: int = -1):
        response = self._manager.get("/messenger/from",
                                     data={"me": me, "user": user, "database_id": database_id})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_messenges_to(self, me: str, user: str, database_id: int = -1):
        response = self._manager.get("/messenger/to",
                                     data={"me": me, "user": user, "database_id": database_id})

        if response.status_code == 200:
            result: list = response.json()
            return result

        raise Exception(response.json()["detail"])

    def database_serialize(self, database_id: int = -1):
        response = self._manager.get(
            "/database_serialize", data={"database_id": database_id})

        if response.status_code == 200:
            result: dict = response.json()
            return result

    def copy_database(self, source: DataBaseUserModel, database_id: int = -1):
        response = self._manager.get(
            "/copy_database", data={"source": source, "database_id": database_id})

        if response.status_code == 200:
            result: dict = response.json()
            return result
