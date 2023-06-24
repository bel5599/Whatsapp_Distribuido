from requests import get, put

from .base_node import BaseNode, BaseNodeModel


class RemoteNode(BaseNode):
    def __init__(self, id: int, ip: str, port: str):
        super().__init__(id, ip, port)
        self.url = f"http://{self.ip}:{self.port}"

    def successor(self):
        response = get(f"{self.url}/successor/")
        response.raise_for_status()

        model = BaseNodeModel(**response.json())
        return RemoteNode.from_base_model(model)

    def predecessor(self):
        response = get(f"{self.url}/predecessor/")
        response.raise_for_status()

        model = BaseNodeModel(**response.json())
        return RemoteNode.from_base_model(model)

    def set_predecessor(self, node: BaseNode):
        response = put(f"{self.url}/predecessor/", data=node.serialize())
        response.raise_for_status()

    def closest_preceding_finger(self, id: int):
        response = get(f"{self.url}/fingers/closest_preceding/{id}")
        response.raise_for_status()

        model = BaseNodeModel(**response.json())
        return RemoteNode.from_base_model(model)

    def find_successor(self, id: int):
        response = get(f"{self.url}/successor/{id}")
        response.raise_for_status()

        model = BaseNodeModel(**response.json())
        return RemoteNode.from_base_model(model)

    def update_fingers(self, node: BaseNode, index: int):
        response = put(f"{self.url}/fingers/update/{index}",
                       data=node.serialize())
        response.raise_for_status()
