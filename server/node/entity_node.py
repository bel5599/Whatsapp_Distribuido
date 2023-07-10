from typing import Union, Any, Literal

from data.database_entity import DataBaseUser
from .models import DataBaseUserModel, MessengesModel, UsersModel
from ..chord.node import Node as ChordNode
from ..util import generate_id
from .base_entity_node import BaseEntityNode


class DatabaseReplica:
    def __init__(self, owner: Union[BaseEntityNode, None], db: Union[DataBaseUser, None]):
        self.owner = owner
        self.db = db


class EntityNode(ChordNode, BaseEntityNode):
    # region RETURN TYPE OVERLOAD
    def successor(self) -> Union[BaseEntityNode, None]:
        successor: Any = super().successor()
        return successor

    def predecessor(self) -> Union[BaseEntityNode, None]:
        predecessor: Any = super().predecessor()
        return predecessor

    def find_successor(self, id: int) -> Union[BaseEntityNode, None]:
        id_successor: Any = super().find_successor(id)
        return id_successor
    # endregion

    def __init__(self, ip: str, port: str, capacity: int):
        super().__init__(ip, port, capacity)

        self.database = DataBaseUser("data")

        # get two predecessors and create replicas
        predecessor, second_predecessor = self._get_predecessors()

        self.replicas = [
            DatabaseReplica(predecessor, predecessor and DataBaseUser(
                "pred_replication_data")),
            DatabaseReplica(second_predecessor, second_predecessor and DataBaseUser(
                "secondpred_replication_data"))
        ]

    def _get_two_nodes(self, direction: Union[Literal["before"], Literal["after"]]):
        # get pred or succ
        accessor_func = self.__class__.successor if direction == "after" else self.__class__.predecessor

        first = accessor_func(self)
        if first and first == self:
            first = None

        if not first:
            return first, None

        # get pred.pred or succ.succ
        accessor_func = first.__class__.successor if direction == "after" else first.__class__.predecessor

        second = accessor_func(first)
        if second and second == self:
            second = None

        return first, second

    def _get_predecessors(self):
        return self._get_two_nodes("before")

    def _get_successors(self):
        return self._get_two_nodes("after")

    def _get_database(self, database_id: int = -1):
        if database_id == -1:
            return self.database

        for replica in self.replicas:
            owner = replica.owner
            if owner and owner.id == database_id:
                return replica.db

    # region USER

    def get_users(self, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.get_users()

        return []

    def add_user(self, nickname: str, password: str, ip: str, port: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            success = db.add_user(nickname, password, ip, port)

            if success and database_id == -1:
                # replicate
                for successor in self._get_successors():
                    if successor:
                        successor.add_user(
                            nickname, password, ip, port, self.id)

            return success

        return False

    def get_pasword(self, nickname: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.get_password(nickname)

        return ""

    def delete_user(self, nickname: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.delete_user(nickname)

        return False

    def update_user(self, nickname: str, ip: str, port: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.update_user(nickname, ip, port)

        return False

    def get_ip_port(self, nickname: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.get_ip_port(nickname)

        return ""

    def _nickname_entity_node_rec(self, nickname: str, node, database_id: int):
        if self.id == node.id:
            return None

        if database_id == -1 and self.database.contain_user(nickname):
            return self

        if self.database.contain_user(nickname) or any([replica.db and replica.db.contain_user(nickname) for replica in self.replicas]):
            return self

        return self.successor._nickname_entity_node_rec(nickname, node, database_id)

    def nickname_entity_node(self, nickname: str, database_id: int):
        if database_id == -1 and self.database.contain_user(nickname):
            return self

        if self.database.contain_user(nickname) or any([replica.db and replica.db.contain_user(nickname) for replica in self.replicas]):
            return self

        return self.successor._nickname_entity_node_rec(nickname, self, database_id)

    def search_entity_node(self, nickname: str):
        id = generate_id(nickname, self.network_capacity())
        return self.find_successor(id)

    # endregion

    # region MESSAGES

    def add_messenges(self, source: str, destiny: str, value: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.add_messenges(source, destiny, value)

        return False

    def delete_messenges(self, id_messenger: int, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.delete_messenges(id_messenger)

        return False

    def search_messenges_from(self, me: str, user: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.search_messenges_from(me, user)

        return []

    def search_messenges_to(self, me: str, user: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.search_messenges_to(me, user)

        return []

    def get_messages(self, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.get_messages()

        return []

    def delete_messenges_to(self, me: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.delete_messenges_to(me)

        return False

    def delete_messenges_from(self, me: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.delete_messenges_from(me)

        return False

    # endregion

    # region REPLICATION

    def database_serialize(self, database_id: int = -1):
        database = self._get_database(database_id)

        user_serialize = []
        messenge_serialize = []
        # lista de tupla con las propiedades de user
        if database:
            users = database.get_users()
            if users is not False:
                for user in users:
                    user_serialize.append(UsersModel(
                        nickname=user[0], password=user[1], ip=user[2], port=user[3]))

            messenges_ = database.get_messages()
            if messenges_ != False:
                for messenge in messenges_:
                    messenge_serialize.append(MessengesModel(
                        messenge_id=messenge[0], user_id_from=messenge[1], user_id_to=messenge[2], value=messenge[3]))

        return DataBaseUserModel(users=user_serialize, messenges=messenge_serialize)
        # return user_serialize,messenge_serialize

    def copy_database(self, model: DataBaseUserModel, database_id: int):
        # lista de usermodel y lista de messengemodel
        # dataBaseUserModel = model.serialize()
        users_serialize = model.users
        messenges_serialize = model.messenges

        my_database = self._get_database(database_id)
        if my_database:
            # Cada user es de tipo usermodel serializado
            for user in users_serialize:
                my_database.add_user(
                    user.nickname, user.password, user.ip, user.port)

            for messenge in messenges_serialize:
                my_database.add_messenges(
                    messenge.user_id_from, messenge.user_id_to, messenge.value)

    # endregion

    def _preserve_replicated_data(self):
        pred_replica = self.replicas[0]
        if not (pred_replica.owner and pred_replica.owner.heart()):
            successor, second_successor = self._get_successors()
            # 1- self.añade_a_mi_db(db)
            # 2- self.successor().replicate(db, self.id)
            # 3- self.successor().successor().replicate(db, self.id)
            pass

    def update_replications(self):
        # como EntityNode mantiene referencias de RemoteNodes que no se actualizan
        # con la estabilizacion, tenemos que actualizarlas nosotros

        # pero antes tenemos que chekear si el nodo en predecessor_replica
        # se ha desconectado, porque habria entonces que guardar su información
        # como propia, y por tanto, replicarla
        self._preserve_replicated_data()

        # hasta aqui ya salvamos la info replicada del nodo que se
        # ha desconectado, y la hemos replicado puesto que es propia ahora

        # procedemos a actualizar las replicas
        old_predecessor, old_second_predecessor = [
            replica.owner for replica in self.replicas]
        old_predecessor_db, old_second_predecessor_db = [
            replica.db for replica in self.replicas]
        predecessor, second_predecessor = self._get_predecessors()
        self.replicas[0].owner = predecessor
        self.replicas[1].owner = second_predecessor

        # decidir si crear/usar existente/borrar la db correspondiente

        if predecessor != old_predecessor:
            if not predecessor:
                # TODO: borrar la db existente
                self.replicas[0].db = None
            elif predecessor == old_second_predecessor:
                self.replicas[0].db = old_second_predecessor_db
            else:
                # TODO: borrar la db existente
                self.replicas[0].db = DataBaseUser("pred_replication_data")

        if second_predecessor != old_second_predecessor:
            if not second_predecessor:
                # TODO: borrar la db existente
                self.replicas[1].db = None
            elif second_predecessor == old_predecessor:
                self.replicas[1].db = old_predecessor_db
            else:
                # TODO: borrar la db existente
                self.replicas[1].db = DataBaseUser(
                    "secondpred_replication_data")
