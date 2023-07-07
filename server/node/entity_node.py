from pydantic import BaseModel

from ..chord.node import Node as ChordNode
from data.database_entity import DataBaseUser
from ..util import generate_id
from .base_entity_node import BaseEntityNode


class MessengerModel(BaseModel):
    source: str
    destiny: str
    value: str
    database_id: int


class UserModel(BaseModel):
    nickname: str
    password: str
    ip: str
    port: str
    database_id: int


class DataBaseModel(BaseModel):
    database_id: int


class SearchMessengerModel(BaseModel):
    source: str
    destiny: str
    database_id: int
    

class CopyDataBaseModel(BaseModel):
    source: DataBaseUser
    database_id: int


class EntityNode(ChordNode, BaseEntityNode):
    def __init__(self, ip: str, port: str, capacity: int):
        super().__init__(ip, port, capacity)
        self.database = DataBaseUser("data")
        # self.replication_database = DataBaseUser("replication_data")

        self.predecessor_replica = (self.predecessor().id, DataBaseUser("replication_data"))
        self.second_predecessor_replica = (self.predecessor().predecessor.id, DataBaseUser("replication_data"))

    # User
    def add_user(self, nickname: str, password: str, ip: str, port: str, database_id: int):
        if database_id == -1:
            return self.database.add_user(nickname, password, ip, port)
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].add_user(nickname, password, ip, port)
        return self.second_predecessor_replica[1].add_user(nickname, password, ip, port)

    def get_users(self, database_id: int):
        if database_id == -1:
            return self.database.get_users()
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].get_users()
        return self.second_predecessor_replica[1].get_users()

    def get_pasword(self, nickname: str, database_id: int):
        if database_id == -1:
            return self.database.get_password(nickname)
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].get_password(nickname)
        return self.second_predecessor_replica[1].get_password(nickname)

    def delete_user(self, nickname: str, database_id: int):
        if database_id == -1:
            return self.database.delete_user(nickname)
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].delete_user(nickname)
        return self.second_predecessor_replica[1].delete_user(nickname)

    def update_user(self, nickname: str, ip: str, port: str, database_id: int):
        if database_id == -1:
            return self.database.update_user(nickname, ip, port)
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].update_user(nickname, ip, port)
        return self.second_predecessor_replica[1].update_user(nickname, ip, port)

    def nickname_entity_node(self, nickname: str, database_id: int):
        if database_id == -1:
            self.database.contain_user(nickname)
            return self
        if self.database.contain_user(nickname) or self.predecessor_replica[1].contain_user(nickname) or self.second_predecessor_replica[1].contain_user(nickname):
            return self

        return self.successor.nickname_entity_node_rec(nickname, self, database_id)

    def nickname_entity_node_rec(self, nickname: str, node, database_id: int):
        if self.id == node.id:
            return None

        if database_id == -1:
            self.database.contain_user(nickname)
            return self
        if self.database.contain_user(nickname) or self.predecessor_replica[1].contain_user(nickname) or self.second_predecessor_replica[1].contain_user(nickname):
            return self
        return self.successor.nickname_entity_node_rec(nickname, node, database_id)

    def search_entity_node(self, nickname: str):
        id = generate_id(nickname, self.network_capacity())
        return self.find_successor(id)

    # MESSENGES

    def add_messenges(self, source: str, destiny: str, value: str, database_id: int):
        if database_id == -1:
            return self.database.add_messenges(source, destiny, value)
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].add_messenges(source, destiny, value)
        return self.second_predecessor_replica[1].add_messenges(source, destiny, value)

    def search_messenges_from(self, me: str, user: str, database_id: int):
        if database_id == -1:
            return self.database.search_messenges_from(me, user)
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].search_messenges_from(me, user)
        return self.second_predecessor_replica[1].search_messenges_from(me, user)

    def search_messenges_to(self, me: str, user: str, database_id: int):
        if database_id == -1:
            return self.database.search_messenges_to(me, user)
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].search_messenges_to(me, user)
        return self.second_predecessor_replica[1].search_messenges_to(me, user)

    def delete_messenges(self, id_messenger: int, database_id: int):
        if database_id == -1:
            return self.database.delete_messenges(id_messenger)
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].delete_messenges(id_messenger)
        return self.second_predecessor_replica[1].delete_messenges(id_messenger)
        
    def copy_database(self, source: DataBaseUser, database_id: int):
        if database_id == -1:
            return self.database.copy_database(source)
        if self.predecessor_replica[0] == database_id:
            return self.predecessor_replica[1].copy_database(source)
        return self.second_predecessor_replica[1].copy_database(source)

    def fix_replications(self):
        # como EntityNode mantiene referencias de RemoteNodes que no se actualizan
        # con la estabilizacion, tenemos que actualizarlas nosotros

        # pero antes tenemos que chekear si el nodo en predecessor_replica
        # se ha desconectado, porque habria entonces que guardar su información
        # como propia, y por tanto, replicarla
        old_predecessor, db = self.predecessor_replica
        if not (old_predecessor and old_predecessor.heart()):
            # 1- self.añade_a_mi_db(db)
            # 2- self.successor().replicate(db, self.id)
            # 3- self.successor().successor().replicate(db, self.id)
            pass

        # hasta aqui ya salvamos la info replicada del nodo que se
        # ha desconectado, y la hemos replicado puesto que es propia ahora

        # procedemos a actualizar las replicas
        pred_replica = self.predecessor_replica
        second_replica = self.second_predecessor_replica

        predecessor = self.predecessor()
        second_predecessor = predecessor and predecessor.predecessor()

        if predecessor and predecessor != pred_replica[0]:
            # va a reemplazarlo, pero con cual db?
            if predecessor == second_replica[0]:
                self.predecessor_replica = (predecessor, second_replica[1])
            else:
                self.predecessor_replica = (predecessor, new_DB)

        if second_predecessor and second_predecessor != second_replica[0]:
            # va a reemplazarlo, pero con cual db?
            if second_predecessor == pred_replica[0]:
                self.second_predecessor_replica = (
                    second_predecessor, pred_replica[1])
            else:
                self.second_predecessor_replica = (second_predecessor, new_DB)

        # listo!

        # TODO: implementar lo que falta en el metodo
