from datetime import*

from db import  Base
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DATETIME, Date



class User(Base):
    __tablename__ = "user_account"
    
    nickname:  Mapped[str] = mapped_column(String(30),unique=True,primary_key=True,nullable=False)
    
    def __repr__(self) -> str:
        return f"User(nickname={self.nickname!r})"

class Messenger(Base):
    __tablename__ = "messenger"
    
    messenger_id: Mapped[int] = mapped_column(primary_key=True)
    user_id_from: Mapped[int] = mapped_column(ForeignKey("user_account.nickname"))
    user_id_to:   Mapped[int] = mapped_column(ForeignKey("user_account.nickname"))
    chat_id:      Mapped[int] = mapped_column(ForeignKey("chat.chat_id"))
    value:        Mapped[str] = mapped_column(String)
    date:         Mapped[datetime] = mapped_column(DATETIME)

    def __repr__(self) -> str:
        return f"Messenger(id={self.messenger_id!r}, user_id_from={self.user_id_from!r}, user_id_to={self.user_id_to!r},chat_id={self.chat_id!r})"


class Chat(Base):
    __tablename__ = "chat"   
    
    chat_id:    Mapped[int] = mapped_column(primary_key=True)
    user_id_1:  Mapped[int] = mapped_column(ForeignKey("user_account.nickname"))
    user_id_2:  Mapped[int] = mapped_column(ForeignKey("user_account.nickname"))
    
    def __repr__(self) -> str:
        return f"Chat(id={self.chat_id!r}, user_id_1={self.user_id_1!r}, user_id_2={self.user_id_2!r})"

    