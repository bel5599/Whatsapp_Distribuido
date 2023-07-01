from requests import get, put

from .base_node import BaseNode, BaseNodeModel


class RemoteNode(BaseNode):
    def __init__(self, id: int, ip: str, port: str):
        super().__init__(id, ip, port)
        self.url = f"http://{self.ip}:{self.port}"

    def network_capacity(self):
        response = get(f"{self.url}/fingers/capacity/")

        if response.status_code == 200:
            capacity: int = response.json()["capacity"]
            return capacity

        raise Exception(response.json()["detail"])

    def successor(self):
        response = get(f"{self.url}/successor/")

        if response.status_code == 200:
            model = BaseNodeModel(**response.json())
            return RemoteNode.from_base_model(model)

        raise Exception(response.json()["detail"])

    def predecessor(self):
        response = get(f"{self.url}/predecessor/")

        if response.status_code == 200:
            model = BaseNodeModel(**response.json())
            return RemoteNode.from_base_model(model)

        raise Exception(response.json()["detail"])

    def set_predecessor(self, node: BaseNode):
        response = put(f"{self.url}/predecessor/", data=node.serialize())

        if response.status_code != 200:
            raise Exception(response.json()["detail"])

    def closest_preceding_finger(self, id: int):
        response = get(f"{self.url}/fingers/closest_preceding/{id}")

        if response.status_code == 200:
            model = BaseNodeModel(**response.json())
            return RemoteNode.from_base_model(model)

        raise Exception(response.json()["detail"])

    def find_successor(self, id: int):
        response = get(f"{self.url}/successor/{id}")

        if response.status_code == 200:
            model = BaseNodeModel(**response.json())
            return RemoteNode.from_base_model(model)

        raise Exception(response.json()["detail"])

    def update_fingers(self, node: BaseNode, index: int):
        response = put(f"{self.url}/fingers/update/{index}",
                       data=node.serialize())

        if response.status_code != 200:
            raise Exception(response.json()["detail"])
        
    def fingers_predecessor_list(self):
        response = get(f"{self.url}/fingers_predecessor")

        if response.status_code == 200:
            result: list = response.json()
            return result
        
        raise Exception(response.json()["detail"])
