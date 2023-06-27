from db import Base,engine,session
from models import*
from sqlalchemy.orm import Session



def create_database():
    Base.metadata.create_all(engine)

# USER 
def add_user(nickname_,password_):
    #si no existe agregalo
    if not contain_user(nickname_):
        with session:
            user = User(
            nickname=nickname_,
            password = password_
            )
            session.add_all([user])
            session.commit()
            return True
    else: return False
        
def contain_user(nickname_):
    contain = session.query(User).get(nickname_)
    return contain is not None 
                           
def delete_user(nickname):
    contain = session.query(User).get(nickname)
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

#Todos los sms que envie, o que envie a user
#Devuelve una lista de tuplas(user_from,Value)
def search_messenger_from(me, user = None):
    
    try:
        if user is None:
            result = session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_from == me).all()
        else:
            result = session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_from == me and Messenger.user_id_to == user).all()
            
        return result
    except:
        return False    

#Todos los sms que me enviaron , o los que me envio user
#Devuelve una lista de tuplas(user_from,Value)
def search_messenger_to(me,user=None):
    try:
        if user is None:
            result = session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_to == me).all()       
        else:
            result = session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_from == user and Messenger.user_id_to == me).all()
            
        return result
    except:
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
        #Elimina todos los sms del chat
        for id in session.query(Messenger).filter(Messenger.chat_id==chat_id).all():
            session.delete(id)
            
        contain = session.query(Chat).get(chat_id)
        session.delete(contain) 
        session.commit()
        return True
    return False