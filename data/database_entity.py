from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Union
from .model_entity import *
# from model_entity import User, Messenge
import time


class DataBaseUser:
    def __init__(self, name: str = 'user_data'):
        engine = create_engine('sqlite:///'+name+'.sqlite',
                               connect_args={"check_same_thread": False})
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)
        self.clear()

    # USER
    # Devuelve una lista:user de todos los usuarios de la base datos
    def get_users(self) -> list[tuple[str, str, str, str]]:
        result = []
        try:
            users = self.session.query(User).all()
            for user in users:
                result.append(
                    (user.nickname, user.password, user.ip, user.port))
            return result
        except:
            return result

    def add_user(self, nickname_: str, password_: str, ip_: str, port_: str) -> bool:
        try:
            with self.session:
                user = User(
                    nickname=nickname_,
                    password=password_,
                    ip=ip_,
                    port=port_
                )
                self.session.add_all([user])
                self.session.commit()
                return True
        except:
            return False

    def contain_user(self, nickname_: str) -> bool:
        contain = self.session.query(User).get(nickname_)
        return contain is not None

    def delete_user(self, nickname: str) -> bool:
        contain = self.session.query(User).get(nickname)
        if contain is not None:
            self.session.delete(contain)
            self.session.commit()
            return True
        return False

    def get_password(self, nickname: str) -> str:
        try:
            password = self.session.query(User).filter(
                User.nickname == nickname).one()
            if password:
                return password.password
            return ' '
        except:
            return ' '

    def update_user(self, nickname: str, ip: str, port: str) -> bool:
        try:
            self.session.query(User).filter(User.nickname == nickname).update(
                {User.ip: ip, User.port: port})
            self.session.commit()
            return True
        except:
            return False

    def get_ip_port(self, nickname: str) -> str:
        user = self.session.query(User).filter(User.nickname == nickname).one()
        return user.ip+':'+user.port

    # MESSENGES
    def get_messages(self) -> list[tuple[int, str, str, str]]:
        result = []
        try:
            message = self.session.query(Message).all()
            for m in message:
                result.append(
                    (m.message_id, m.user_id_from, m.user_id_to, m.value))
            return result
        except:
            return result

    def contain_messages(self, id, source: str, destiny: str, value: str) -> bool:
        contain = self.session.query(Message).filter(Message.message_id == id, Message.user_id_from ==
                                                     source, Message.user_id_to == destiny, Message.value == value).first()
        return contain is not None

    def add_messages(self, source: str, destiny: str, value_: str, id=-1) -> bool:
        # Crear el chat si no existe y luego agregarselo a la tabla
        # Crear el chat si no existe y luego agregarselo a la tabla
        if id == -1:
            id_ = int(time.time())
        else:
            id_ = id

        if self.contain_messages(id_, source, destiny, value_):
            return False
        try:
            with self.session:
                messages = Message(
                    message_id=id_,
                    user_id_from=source,
                    user_id_to=destiny,
                    value=value_,)
                # if messages is Message:
                self.session.add_all([messages])
                self.session.commit()
                return True
        except:
            return False

        # Se podria coger la fecha y hora de la computadora en el momento que se usa el m\'etodo

    def delete_messages(self, id_message: int) -> bool:
        message = self.session.query(Message).get(id_message)
        if message is not None:
            self.session.delete(message)
            self.session.commit()
            return True
        return False

    # Todos los sms que envie, o que envie a user
    # Devuelve una lista de tuplas(user_from,Value)
    def search_messages_from(self, me: str, user: str = '') -> list[tuple[str, str]]:
        result = []
        try:
            if user == ' ':
                query = self.session.query(Message).filter(
                    Message.user_id_from == me).all()
            else:
                query = self.session.query(Message).filter(
                    Message.user_id_from == me, Message.user_id_to == user).all()
            for q in query:
                result.append((q.user_id_from, q.value))
            return result
        except:
            return result

    # Todos los sms que me enviaron , o los que me envio user
    # Devuelve una lista de tuplas(user_from,Value)
    def search_messages_to(self, me: str) -> list[tuple[str, str]]:
        result = []
        try:
            query = self.session.query(Message).filter(
                Message.user_id_to == me).all()

            for q in query:
                result.append((q.user_id_from, q.value))
            return result
        except:
            return []

    def delete_messages_to(self, me: str) -> bool:
        try:
            result = self.session.query(Message).filter(
                Message.user_id_to == me).all()
            for r in result:
                self.session.delete(r)
                self.session.commit()
            return True
        except:
            return False

    def delete_messages_from(self, me: str) -> bool:
        try:
            result = self.session.query(Message).filter(
                Message.user_id_from == me).all()
            for r in result:
                self.session.delete(r)
                self.session.commit()
            return True
        except:
            return False

    def clear(self) -> bool:
        try:
            messages = self.session.query(Message).all()
            users = self.session.query(User).all()
            for m in messages:
                self.session.delete(m)
                self.session.commit()
            for u in users:
                self.session.delete(u)
                self.session.commit()
            return True
        except:
            return False
