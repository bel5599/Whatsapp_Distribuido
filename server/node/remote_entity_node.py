from ..chord.remote_node import RemoteNode as ChordRemoteNode


class RemoteEntityNode(ChordRemoteNode):

    #User
    def add_user(self, nickname: str, pasword: str,  ip: str, port: str, database_original: bool):
        response = self._manager.put(
            "/user/add", data={"nickname": nickname, "pasword": pasword, "ip": ip, "port": port, "database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])
    
    def get_pasword(self, nickname: str, database_original: bool):
        response = self._manager.get(f"/user/pasword/{nickname}", data = {"database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result
        
        raise Exception(response.json()["detail"])

    def nickname_entity_node(self, nickname: str, database_original: bool=False):
        response = self._manager.get(f"/info/entity/{nickname}", data = {"database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])
    
    def search_entity_node(self, nickname: str, database_original: bool):
        response = self._manager.get(f"/info/search_entity/{nickname}", data = {"database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def delete_user(self, nickname: str, database_original: bool):
        response = self._manager.delete(f"/user/delete/{nickname}", data = {"database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    # MESSENGES
    def add_messenges(self, source: str, destiny: str, value: str, database_original: bool):
        response = self._manager.put("/messenger/add",
                                     data={"source": source, "destiny": destiny, "value": value, "database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def delete_messenges(self, id: int, database_original: bool):
        response = self._manager.delete(f"/messenger/delete/{id}", data = {"database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_messenges_from(self, me: str, user: str, database_original: bool):
        response = self._manager.get("/messenger/from",
                                     data={"me": me, "user": user, "database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_messenges_to(self, me: str, user: str, database_original: bool):
        response = self._manager.get("/messenger/to",
                                     data={"me": me, "user": user, "database_original": database_original})

        if response.status_code == 200:
            result: list = response.json()
            return result

        raise Exception(response.json()["detail"])

    

