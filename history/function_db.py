from db import Base,engine,session
from models import*
from sqlalchemy.orm import Session
from sqlalchemy import select


def create_database():
    Base.metadata.create_all(engine)

# USER
def add_user(nickname_):
    with session:
        user = User(
            nickname=nickname_,
        )
        session.add_all([user])
        session.commit()

                       
def delete_user():
    pass


# MESSENGER
def add_messenger(source,destiny,value_):
    # Crear el chat si no existe y luego agregarselo a la tabla 
    idChat = search_chat_id(source,destiny)
    
    if idChat is None:
        add_chat(source,destiny)
        
    #Falta actualizar idchat    
    
    with Session(engine) as session:
        messenger = Messenger(
            user_id_from= source,
            user_id_to  = destiny,   
            chat_id     = idChat,      
            value       = value_,        
        )
        
        session.add_all([messenger])
        session.commit()
    # Se podria coger la fecha y hora de la computadora en el momento que se usa el m\'etodo
    
def delete_messenger():
    pass


# CHAT
def add_chat(user_id_1_,user_id_2_):
    with Session(engine) as session:
        chat = Chat(
            user_id_1=user_id_1_,
            user_id_2=user_id_2_,
        )
        session.add_all([chat])
        session.commit()


def search_chat_id(user_id_1,user_id_2):
    stmt = select(Chat).where(Chat.user_id_1.is_(user_id_1) and Chat.user_id_2.is_(user_id_2) or 
                              Chat.user_id_1.is_(user_id_2) and Chat.user_id_2.is_(user_id_1)  )
    
    for chat in session.scalars(stmt):
        return chat.id

    

        
def delete_chat():
    pass
