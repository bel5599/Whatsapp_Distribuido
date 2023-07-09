# type: ignore
from datetime import*
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String, Float, DATETIME, Date

Base = declarative_base()

class Contacts(Base):
    __tablename__ = "contacts"
    id_contact :    Mapped[int] = Column(Integer,primary_key=True)
    nickname:       Mapped[str] = Column(String(30),nullable=False)
    mynickname:     Mapped[str] = Column(String(30),nullable =False)
    name:           Mapped[str] = Column(String) 
    
    def __repr__(self) -> str:
        return f"User(nickname={self.nickname!r},mynickname={self.mynickname!r},name_contact={self.name!r})"


class Messenge(Base):
    __tablename__ = "messenges"
    
    messenger_id: Mapped[int] = Column(Integer,primary_key=True)
    user_id_from: Mapped[str] = Column(String(30))
    user_id_to:   Mapped[str] = Column(String(30))
    chat_id:      Mapped[int] = Column(ForeignKey("chat.chat_id"))
    value:        Mapped[str] = Column(String)
    #date:         Mapped[datetime] = Column(DATETIME)

    def __repr__(self) -> str:
        return f"Messenge(id={self.messenger_id!r}, user_id_from={self.user_id_from!r}, user_id_to={self.user_id_to!r},chat_id={self.chat_id!r},value={self.value!r})"


class Chat(Base):
    __tablename__ = "chat"   
    
    chat_id:    Mapped[int] = Column(Integer,primary_key=True)
    user_id_1:  Mapped[str] = Column(String(30))
    user_id_2:  Mapped[str] = Column(String(30))
    
    def __repr__(self) -> str:
        return f"Chat(id={self.chat_id!r}, user_id_1={self.user_id_1!r}, user_id_2={self.user_id_2!r})"