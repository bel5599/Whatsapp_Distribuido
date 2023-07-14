from typing import Union, Any, Literal

from data.database_entity import DataBaseUser
from .models import DataBaseUserModel, DataMessagesModel, DataUsersModel
from ..chord.node import Node as ChordNode
from ..chord.remote_node import RemoteNode as ChordRemoteNode
from ..util import generate_id
from .base_entity_node import BaseEntityNode
from .remote_entity_node import RemoteEntityNode


class DatabaseReplica:
    def __init__(self, owner: Union[BaseEntityNode, None], db: DataBaseUser):
        self.owner = owner
        self.db = db


class EntityNode(ChordNode, BaseEntityNode):
    # region RETURN TYPE OVERLOAD
    def successor(self) -> Union[BaseEntityNode, None]:
        successor: Any = super().successor()
        if isinstance(successor, ChordRemoteNode):
            return RemoteEntityNode.from_remote_node(successor)

        return successor

    def predecessor(self) -> Union[BaseEntityNode, None]:
        predecessor: Any = super().predecessor()
        if isinstance(predecessor, ChordRemoteNode):
            return RemoteEntityNode.from_remote_node(predecessor)

        return predecessor

    def find_successor(self, id: int) -> Union[BaseEntityNode, None]:
        id_successor: Any = super().find_successor(id)
        if isinstance(id_successor, ChordRemoteNode):
            return RemoteEntityNode.from_remote_node(id_successor)

        return id_successor
    # endregion

    def __init__(self, ip: str, port: str, capacity: int):
        super().__init__(ip, port, capacity)

        self.database = DataBaseUser("data")

        # get two predecessors and create replicas
        predecessor, second_predecessor = self._get_predecessors()

        self.replicas = [
            DatabaseReplica(predecessor, DataBaseUser(
                "pred_replication_data")),
            DatabaseReplica(second_predecessor, DataBaseUser(
                "secondpred_replication_data"))
        ]

    def _get_two_nodes(self, direction: Union[Literal["before"], Literal["after"]]):
        first = self.successor() if direction == "after" else self.predecessor()
        if first and first == self:
            first = None

        if not first:
            return first, None

        second = first.successor() if direction == "after" else first.predecessor()
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
            success = db.update_user(nickname, ip, port)
            if success and database_id == -1:
                # replicate
                for successor in self._get_successors():
                    if successor:
                        successor.update_user(
                            nickname, ip, port, self.id)
            return success
        return False

    def get_ip_port(self, nickname: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.get_ip_port(nickname)

        return ""

    def nickname_entity_node(self, nickname: str, search_id: int = -1):
        # dio la vuelta y llego al nodo q empezo la busqueda
        if search_id == self.id:
            return None

        # if search_id == -1 => self empieza la busqueda
        # de lo contrario ya esta en la busqueda
        search_id = self.id if search_id == -1 else search_id

        # buscar en el nodo actual
        if self.database.contain_user(nickname) or any([replica.db and replica.db.contain_user(nickname) for replica in self.replicas]):
            return self

        # no lo encontramos aqui, buscar en el successor
        successor = self.successor()
        return successor and successor.nickname_entity_node(nickname, search_id)

    def search_entity_node(self, nickname: str):
        id = generate_id(nickname, self.network_capacity())
        return self.find_successor(id)

    # endregion

    # region MESSAGES

    def add_messages(self, source: str, destiny: str, value: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            success = db.add_messages(source, destiny, value)
            if success and database_id == -1:
                # replicate
                for successor in self._get_successors():
                    if successor:
                        successor.add_messages(
                            source, destiny, value, self.id)

            return success
        return False

    def search_messages_to(self, me: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            return db.search_messages_to(me)

        return []

    def delete_messages_to(self, me: str, database_id: int):
        db = self._get_database(database_id)
        if db:
            success = db.delete_messages_to(me)
            if success and database_id == -1:
                # replicate
                for successor in self._get_successors():
                    if successor:
                        successor.delete_messages_to(me, self.id)
            return success

        return False

    # endregion

    # region REPLICATION

    def get_replication_data(self):
        return self._prepare_replication_data(self.database)

    def replicate(self, data: DataBaseUserModel, database_id: int):
        # lista de usermodel y lista de messengemodel
        # dataBaseUserModel = model.serialize()
        users_serialize = data.users
        messages_serialize = data.messages

        db = self._get_database(database_id)
        if db:
            # Cada user es de tipo usermodel serializado
            for user in users_serialize:
                db.add_user(
                    user.nickname, user.password, user.ip, user.port)

            for message in messages_serialize:
                db.add_messages(
                    message.user_id_from, message.user_id_to, message.value)

    # endregion

    @staticmethod
    def _prepare_replication_data(database: DataBaseUser):
        user_serialize = []
        message_serialize = []
        # lista de tupla con las propiedades de user
        if database:
            users = database.get_users()
            if users is not False:
                for user in users:
                    user_serialize.append(DataUsersModel(
                        nickname=user[0], password=user[1], ip=user[2], port=user[3]))

            messages_ = database.get_messages()
            if messages_ != False:
                for message in messages_:
                    message_serialize.append(DataMessagesModel(
                        message_id=message[0], user_id_from=message[1], user_id_to=message[2], value=message[3]))

        return DataBaseUserModel(users=user_serialize, messages=message_serialize)

    def _preserve_replication_data(self):
        pred_replica = self.replicas[0]
        if not (pred_replica.owner and pred_replica.owner.heart()):
            data = self._prepare_replication_data(pred_replica.db)

            self.replicate(data, -1)
            successor, second_successor = self._get_successors()
            if successor:
                successor.replicate(data, self.id)
            if second_successor:
                second_successor.replicate(data, self.id)

    def update_replications(self):
        # como EntityNode mantiene referencias de RemoteNodes que no se actualizan
        # con la estabilizacion, tenemos que actualizarlas nosotros

        # pero antes tenemos que chekear si el nodo en predecessor_replica
        # se ha desconectado, porque habria entonces que guardar su información
        # como propia, y por tanto, replicarla
        self._preserve_replication_data()

        # hasta aqui ya salvamos la info replicada del nodo que se
        # ha desconectado, y la hemos replicado puesto que es propia ahora
        old_owners = [replica.owner for replica in self.replicas]
        new_owners = [owner for owner in self._get_predecessors()]

        new_replica_data_list: list[Union[DataBaseUserModel, None]] = []

        for k, (new_owner, old_owner) in enumerate(zip(new_owners, old_owners)):
            if new_owner != old_owner:
                self.replicas[k].owner = new_owner

                # current replica owner changed
                # so its db data could be too

                if not new_owner:
                    self.replicas[k].db.clear()

                # decide which data will be in new owner replica
                elif new_owner == old_owners[1-k]:
                    # will be other owner replica data
                    new_replica_data_list.append(
                        self._prepare_replication_data(self.replicas[1-k].db))
                    continue

                else:
                    new_replica_data_list.append(
                        new_owner.get_replication_data())
                    continue

            new_replica_data_list.append(None)

        # replica owners are set already
        for replica, data in zip(self.replicas, new_replica_data_list):
            if replica.owner and data:
                replica.db.clear()
                self.replicate(data, replica.owner.id)

    def all_nodes(self, search_id: int = -1) -> list[BaseEntityNode]:
        if search_id == self.id:
            return []

        search_id = self.id if search_id == -1 else search_id

        successor = self.successor()
        if successor and successor.heart():
            return [self, *successor.all_nodes(search_id)]

        return [self]
