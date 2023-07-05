from ..chord.remote_node import RemoteNode as ChordRemoteNode


class RemoteEntityNode(ChordRemoteNode):

    def add_user(self, nickname: str, pasword: str, database_original: bool):
        response = self._manager.put(
            "/user/add", data={"nickname": nickname, "pasword": pasword, "database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])
    
    def get_pasword(self, nickname, database_original: bool):
        response = self._manager.get(f"/user/pasword/{nickname}", data = {"database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result
        
        raise Exception(response.json()["detail"])

    def nickname_entity_node(self, nickname, database_original: bool):
        response = self._manager.get(f"/info/entity/{nickname}", data = {"database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])
    
    def search_entity_node(self, nickname, database_original: bool):
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

    def add_messenger(self, source, destiny, value, database_original: bool):
        response = self._manager.put("/messenger/add",
                                     data={"source": source, "destiny": destiny, "value": value, "database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def delete_messenger(self, id: int, database_original: bool):
        response = self._manager.delete(f"/messenger/delete/{id}", data = {"database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_messenger_from(self, me, user, database_original: bool):
        response = self._manager.get("/messenger/from",
                                     data={"me": me, "user": user, "database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_messenger_to(self, me, user, database_original: bool):
        response = self._manager.get("/messenger/to",
                                     data={"me": me, "user": user, "database_original": database_original})

        if response.status_code == 200:
            result: list = response.json()
            return result

        raise Exception(response.json()["detail"])

    def add_chat(self, user_id_1, user_id_2, database_original: bool):
        response = self._manager.put("/chat/add",
                                     data={"user_id_1": user_id_1, "user_id_2": user_id_2, "database_original": database_original})

        if response.status_code == 200:
            result: list = response.json()
            return result

        raise Exception(response.json()["detail"])

    def search_chat_id(self, user_id_1, user_id_2, database_original: bool):
        response = self._manager.get("/chat",
                                     data={"user_id_1": user_id_1, "user_id_2": user_id_2, "database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])
    
    def search_chat(self, user_id_1, user_id_2, database_original: bool):
        response = self._manager.get(f"/chat/search", data = {"user_id_1": user_id_1, "user_id_2": user_id_2, "database_original": database_original})

        if response.status_code == 200:
            result: list = response.json()
            return result
        
        raise Exception(response.json()["detail"])

    def delete_chat(self, user_id_1, user_id_2, database_original: bool):
        response = self._manager.delete(f"/chat/delete", data = {"user_id_1": user_id_1, "user_id_2": user_id_2, "database_original": database_original})

        if response.status_code == 200:
            result: dict = response.json()
            return result

        raise Exception(response.json()["detail"])

    def fingers_predecessor_list(self):
        response = self._manager.get("/info/fingers_predecessor")

        if response.status_code == 200:
            result: list = response.json()
            return result

        raise Exception(response.json()["detail"])
    

    

