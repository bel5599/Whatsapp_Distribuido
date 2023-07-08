from typing import Union

from service.requests import RequestManager
from .base_node import BaseNode, BaseNodeModel
from .node import Node


class RemoteNode(BaseNode):
    def __init__(self, id: int, ip: str, port: str):
        super().__init__(id, ip, port)
        self._manager = RequestManager(ip, port)
        self._local_node: Union[Node, None] = None

    def _ensure_local(self, node: "RemoteNode") -> BaseNode:
        if not self._local_node:
            return node

        if self._local_node == node:
            return self._local_node

        node.set_local_node(self._local_node)
        return node

    def set_local_node(self, node: Node):
        self._local_node = node

    def network_capacity(self):
        response = self._manager.get("/chord/capacity/")

        if response.status_code == 200:
            capacity = int(response.json())
            return capacity

        raise Exception(response.json()["detail"])

    def successor(self):
        try:
            response = self._manager.get("/chord/successor/")
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return self._ensure_local(self.__class__.from_base_model(model))

            print("ERROR:", response.json()["detail"])

    def set_successor(self, node: BaseNode):
        try:
            response = self._manager.put(
                "/chord/successor/", data=node.serialize())
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code != 200:
                print("ERROR:", response.json()["detail"])

    def predecessor(self):
        try:
            response = self._manager.get("/chord/predecessor/")
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return self._ensure_local(self.__class__.from_base_model(model))

            print("ERROR:", response.json()["detail"])

    def set_predecessor(self, node: BaseNode):
        try:
            response = self._manager.put(
                "/chord/predecessor/", data=node.serialize())
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code != 200:
                print("ERROR:", response.json()["detail"])

    def closest_preceding_finger(self, id: int):
        try:
            response = self._manager.get(
                f"/chord/fingers/closest_preceding/{id}")
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return self._ensure_local(self.__class__.from_base_model(model))

            print("ERROR:", response.json()["detail"])

    def find_successor(self, id: int):
        try:
            response = self._manager.get(f"/chord/successor/{id}")
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return self._ensure_local(self.__class__.from_base_model(model))

            print("ERROR:", response.json()["detail"])

    def notify(self, node: BaseNode):
        try:
            response = self._manager.put(
                "/chord/notify/", data=node.serialize())
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code != 200:
                print("ERROR:", response.json()["detail"])

    def heart(self):
        try:
            response = self._manager.get("/chord/heart/")
        except Exception as e:
            print("ERROR:", e)
        else:
            if response.status_code == 200:
                return str(response.json())
