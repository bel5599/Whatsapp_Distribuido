from db import Base,engine,session
from models import*
from sqlalchemy.orm import Session
from sqlalchemy import select


def create_database():
    Base.metadata.create_all(engine)

# USER 
def add_user(nickname_):
    #si no existe agregalo
    if not contain_user(nickname_):
        with session:
            user = User(
            nickname=nickname_,
            )
            session.add_all([user])
            session.commit()
            return True
    else: return False
        
def contain_user(nickname_):
    contain = session.query(User).get(nickname_)
    return contain is not None 
                           
def delete_user(nickname_):
    contain = session.query(User).get(nickname_)
    if contain is not None:
        session.delete(contain) 
        session.commit()
        return True
    return False


# MESSENGER
def add_messenger(source,destiny,value_):
    # Crear el chat si no existe y luego agregarselo a la tabla 
    add_chat(source,destiny)    
    idChat = search_chat_id(source,destiny)
    
    with session:
        messenger = Messenger(
            user_id_from= source,
            user_id_to  = destiny,   
            chat_id     = idChat,      
            value       = value_,        
        )    
        session.add_all([messenger])
        session.commit()
        return True
    # Se podria coger la fecha y hora de la computadora en el momento que se usa el m\'etodo
    
def delete_messenger(id_messenger):
    messenger = session.query(Messenger).get(id_messenger)
    if messenger is not None:
        session.delete(messenger) 
        session.commit()
        return True
    return False


# CHAT
def add_chat(user_id_1_,user_id_2_):
    if search_chat_id(user_id_1_,user_id_2_) is False:
        with session:
            chat = Chat(
            user_id_1=user_id_1_,
            user_id_2=user_id_2_,
            )
            session.add_all([chat])
            session.commit()
            return True
    else: return False

def search_chat_id(user_id_1,user_id_2):
    
    # stmt = select(Chat).where(Chat.user_id_1.is_(user_id_1) and Chat.user_id_2.is_(user_id_2) or 
    #                           Chat.user_id_1.is_(user_id_2) and Chat.user_id_2.is_(user_id_1)  )
    
    # for chat in session.scalars(stmt):
    #     return chat.id
    
    try:
        chat = session.query(Chat).filter(Chat.user_id_1 == user_id_1 and Chat.user_id_2==user_id_2 ).one()
        return chat.chat_id
    except:
        try:
            chat = session.query(Chat).filter(Chat.user_id_1 == user_id_2 and Chat.user_id_2==user_id_1 ).one()
            return chat.chat_id
        except:
            return False
               
def delete_chat(user_id_1,user_id_2):
    chat_id = search_chat_id(user_id_1,user_id_2)
    if chat_id is not False:
        contain = session.query(Chat).get(chat_id)
        session.delete(contain) 
        session.commit()
        return True
    return False