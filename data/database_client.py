from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_client import *
from typing import Union


class DataBaseClient:
    def __init__(self, name: str = 'client_data'):
        engine = create_engine('sqlite:///'+name+'.sqlite')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    # Contacts
    # Devuelve una lista:Contacts de todos los usuarios en la base datos
    def get_contacts(self, mynickname: str) -> list[tuple[str, str]]:
        result = []
        try:
            contacts = self.session.query(Contacts).filter(
                Contacts.mynickname == mynickname and Contacts.name != "Unknown").all()
            for c in contacts:
                result.append((c.nickname, c.name))
            return result
        except:
            return result

    def add_contacts(self, mynickname_: str, nickname_: str, name_: str = "Unknown") -> bool:
        if self.contain_contact(mynickname_, nickname_):
            return False
        try:
            with self.session:
                contact = Contacts(
                    nickname=nickname_,
                    mynickname=mynickname_,
                    name=name_)
                self.session.add_all([contact])
                self.session.commit()
                return True
        except:
            return False

    def update_contact(self, mynickname: str, nickname: str, name: str) -> bool:
        try:
            self.session.query(Contacts).filter(
                Contacts.mynickname == mynickname and Contacts.nickname == nickname).update({Contacts.name: name})
            self.session.commit()
            return True
        except:
            return False

    def contain_contact(self, mynickname: str, nickname: str) -> bool:
        contain = self.session.query(Contacts).filter(
            Contacts.mynickname == mynickname and Contacts.nickname == nickname).first()
        return contain is not None

    def delete_contact(self, mynickname: str, nickname: str) -> bool:
        contain = self.session.query(Contacts).filter(
            Contacts.mynickname == mynickname and Contacts.nickname == nickname).first()
        if contain is not None:
            self.session.delete(contain)
            self.session.commit()
            return True
        return False

    def get_name(self, mynickname: str, nickname: str) -> str:
        name = self.session.query(Contacts).filter(
            Contacts.mynickname == mynickname and Contacts.nickname == nickname).one()
        return name.name

    def get_nickname(self, mynickname: str, name: str) -> str:
        nickname = self.session.query(Contacts).filter(
            Contacts.mynickname == mynickname and Contacts.name == name).one()
        return nickname.nickname

    def get_id(self, mynickname: str, name: str) -> int:
        id = self.session.query(Contacts).filter(
            Contacts.mynickname == mynickname and Contacts.name == name).one()
        return id.id_contact

    # MESSENGER
    def get_messages(self) -> list[tuple[int, str, str, str]]:
        result = []
        try:
            messenge = self.session.query(Messenge).all()
            for m in messenge:
                result.append(
                    (m.messenge_id, m.user_id_from, m.user_id_to, m.value))
            return result
        except:
            return result

    def add_messenges(self, source: str, destiny: str, value_: str, id: int = -1) -> bool:
        # Crear el chat si no existe y luego agregarselo a la tabla
        self.add_chat(source, destiny)
        idChat = self.search_chat_id(source, destiny)
        try:
            with self.session:
                if id != -1:
                    messenger = Messenge(
                        messenger_id=id,
                        user_id_from=source,
                        user_id_to=destiny,
                        chat_id=idChat,
                        value=value_,)
                else:
                    messenger = Messenge(
                        user_id_from=source,
                        user_id_to=destiny,
                        chat_id=idChat,
                        value=value_,)

                self.session.add_all([messenger])
                self.session.commit()
                return True
        except:
            return False

        # Se podria coger la fecha y hora de la computadora en el momento que se usa el m\'etodo

    def delete_messenges(self, id_messenge: int) -> bool:
        messenge = self.session.query(Messenge).get(id_messenge)
        if messenge is not None:
            self.session.delete(messenge)
            self.session.commit()
            return True
        return False

    # Todos los sms que envie, o que envie a user
    # Devuelve una lista de tuplas(user_from,Value)
    def search_messenges_from(self, me: str, user: str = '') -> list[tuple[str, str]]:
        result = []
        try:
            if user == ' ':
                query = self.session.query(Messenge).filter(
                    Messenge.user_id_from == me).all()
            else:
                query = self.session.query(Messenge).filter(
                    Messenge.user_id_from == me and Messenge.user_id_to == user).all()
            for q in query:
                result.append((q.user_id_from, q.value))
            return result
        except:
            return result

    # Todos los sms que me enviaron , o los que me envio user
    # Devuelve una lista de tuplas(user_from,Value)
    def search_messenges_to(self, me: str, user: str = ' ') -> list[tuple[str, str]]:
        result = []
        try:
            if user == ' ':
                query = self.session.query(Messenge).filter(
                    Messenge.user_id_to == me).all()
            else:
                query = self.session.query(Messenge).filter(
                    Messenge.user_id_from == user and Messenge.user_id_to == me).all()
            for q in query:
                result.append((q.user_id_from, q.value))

            return result
        except:
            return []

    # CHAT
    def get_chat(self,mynickname:str)->list[str]:
        result = []
        chats = self.session.query(Chat).filter(Chat.user_id_1 == mynickname or Chat.user_id_2 == mynickname).all()
        for chat in chats:
            if chat.user_id_1 != mynickname:
                user = chat.user_id_1
            else:
                user = chat.user_id_2     
            result.append(user)
        return result
    
    def add_chat(self, user_id_1_: str, user_id_2_: str) -> bool:
        # if  self.search_chat_id(user_id_1_,user_id_2_) is False:
        try:
            with self.session:
                chat = Chat(
                    user_id_1=user_id_1_,
                    user_id_2=user_id_2_,
                )
                self.session.add_all([chat])
                self.session.commit()
                return True
        except:
            return False

    def search_chat_id(self, user_id_1: str, user_id_2: str) -> int:
        try:
            chat = self.session.query(Chat).filter(
                Chat.user_id_1 == user_id_1 and Chat.user_id_2 == user_id_2).one()
            return chat.chat_id
        except:
            try:
                chat = self.session.query(Chat).filter(
                    Chat.user_id_1 == user_id_2 and Chat.user_id_2 == user_id_1).one()
                return chat.chat_id
            except:
                return -1

    def delete_chat(self, user_id_1: str, user_id_2: str) -> bool:
        chat_id = self.search_chat_id(user_id_1, user_id_2)
        if chat_id is not False:
            # Elimina todos los sms del chat
            for id in self.session.query(Messenge).filter(Messenge.chat_id == chat_id).all():
                self.session.delete(id)

            contain = self.session.query(Chat).get(chat_id)
            self.session.delete(contain)
            self.session.commit()
            return True
        return False

    def search_chat(self, user_id_1: str, user_id_2: str) -> list[tuple[str, str]]:
        chat_id = self.search_chat_id(user_id_1, user_id_2)
        result = []
        if chat_id != -1:
            query = self.session.query(Messenge).filter(
                Messenge.chat_id == chat_id).all()
            if query:
                for q in query:
                    result.append((q.user_id_from, q.value))
        return result
