from service.requests import RequestManager
from .base_node import BaseNode, BaseNodeModel


class RemoteNode(BaseNode):
    def __init__(self, id: int, ip: str, port: str):
        super().__init__(id, ip, port)
        self._manager = RequestManager(ip, port)

    def network_capacity(self):
        response = self._manager.get("/fingers/capacity/")

        if response.status_code == 200:
            capacity: int = response.json()["capacity"]
            return capacity

        raise Exception(response.json()["detail"])

    def successor(self):
        response = self._manager.get("/successor/")

        if response.status_code == 200:
            model = BaseNodeModel(**response.json())
            return RemoteNode.from_base_model(model)

        raise Exception(response.json()["detail"])

    def predecessor(self):
        response = self._manager.get("/predecessor/")

        if response.status_code == 200:
            model = BaseNodeModel(**response.json())
            return RemoteNode.from_base_model(model)

        raise Exception(response.json()["detail"])

    def set_predecessor(self, node: BaseNode):
        response = self._manager.put("/predecessor/", data=node.serialize())

        if response.status_code != 200:
            raise Exception(response.json()["detail"])

    def closest_preceding_finger(self, id: int):
        response = self._manager.get(f"/fingers/closest_preceding/{id}")

        if response.status_code == 200:
            model = BaseNodeModel(**response.json())
            return RemoteNode.from_base_model(model)

        raise Exception(response.json()["detail"])

    def find_successor(self, id: int):
        response = self._manager.get(f"/successor/{id}")

        if response.status_code == 200:
            model = BaseNodeModel(**response.json())
            return RemoteNode.from_base_model(model)

        raise Exception(response.json()["detail"])

    def update_fingers(self, node: BaseNode, index: int):
        response = self._manager.put(f"/fingers/update/{index}",
                                     data=node.serialize())

        if response.status_code != 200:
            raise Exception(response.json()["detail"])
