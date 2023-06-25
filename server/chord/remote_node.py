from requests import get, put

from .base_node import BaseNode, BaseNodeModel


class RemoteNode(BaseNode):
    def __init__(self, id: int, ip: str, port: str):
        super().__init__(id, ip, port)
        self.url = f"http://{self.ip}:{self.port}"

    def network_capacity(self):
        try:
            response = get(f"{self.url}/fingers/capacity/")
        except:
            pass
        else:
            if response.status_code == 200:
                capacity: int = response.json()["capacity"]
                return capacity

    def successor(self):
        try:
            response = get(f"{self.url}/successor/")
        except:
            pass
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return RemoteNode.from_base_model(model)

    def predecessor(self):
        try:
            response = get(f"{self.url}/predecessor/")
        except:
            pass
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return RemoteNode.from_base_model(model)

    def set_predecessor(self, node: BaseNode):
        try:
            response = put(f"{self.url}/predecessor/", data=node.serialize())
        except:
            return False
        else:
            return response.status_code == 200

    def closest_preceding_finger(self, id: int):
        try:
            response = get(f"{self.url}/fingers/closest_preceding/{id}")
        except:
            pass
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return RemoteNode.from_base_model(model)

    def find_successor(self, id: int):
        try:
            response = get(f"{self.url}/successor/{id}")
        except:
            pass
        else:
            if response.status_code == 200:
                model = BaseNodeModel(**response.json())
                return RemoteNode.from_base_model(model)

    def update_fingers(self, node: BaseNode, index: int):
        try:
            response = put(f"{self.url}/fingers/update/{index}",
                           data=node.serialize())
        except:
            return False
        else:
            return response.status_code == 200
