from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import*

class DataBase:
    def __init__(self,name:str = 'data'):
        engine = create_engine('sqlite:///'+name+'.sqlite')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.Base = declarative_base()
        Base.metadata.create_all(engine)

    # USER 
    def add_user(self,nickname_,password_):
        #si no existe agregalo
        if not self.contain_user(nickname_):
            with self.session:
                user = User(
                nickname=nickname_,
                password = password_)
                self.session.add_all([user])
                self.session.commit()
                return True
        return False
        
    def contain_user(self,nickname_):
        contain = self.session.query(User).get(nickname_)
        return contain is not None 
                           
    def delete_user(self,nickname):
        contain = self.session.query(User).get(nickname)
        if contain is not None:
            self.session.delete(contain) 
            self.session.commit()
            return True
        return False

    def get_password(self,nickname):
        password = self.session.query(User.password).filter(User.nickname==nickname).one()
        return password[0]
    
    # MESSENGER
    def add_messenger(self,source,destiny,value_):
        # Crear el chat si no existe y luego agregarselo a la tabla 
        self.add_chat(source,destiny)    
        idChat = self.search_chat_id(source,destiny)
        with self.session:
            messenger = Messenger(
            user_id_from= source,
            user_id_to  = destiny,   
            chat_id     = idChat,      
            value       = value_,  )    
            self.session.add_all([messenger])
            self.session.commit()
            return True
        # Se podria coger la fecha y hora de la computadora en el momento que se usa el m\'etodo
        
    def delete_messenger(self,id_messenger):
        messenger = self.session.query(Messenger).get(id_messenger)
        if messenger is not None:
            self.session.delete(messenger) 
            self.session.commit()
            return True
        return False

    # Todos los sms que envie, o que envie a user
    # Devuelve una lista de tuplas(user_from,Value)
    def search_messenger_from(self,me, user = None):
        try:
            if user is None:
                result = self.session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_from == me).all()
            else:
                result = self.session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_from == me and Messenger.user_id_to == user).all()
            
            return result
        except:
            return []    

    # Todos los sms que me enviaron , o los que me envio user
    # Devuelve una lista de tuplas(user_from,Value)
    def search_messenger_to(self,me,user=None):
        try:
            if user is None:
                result = self.session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_to == me).all()       
            else:
                result = self.session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_from == user and Messenger.user_id_to == me).all()
                return result
        except:
            return []   
    
    # CHAT
    def add_chat(self,user_id_1_,user_id_2_):
        if  self.search_chat_id(user_id_1_,user_id_2_) is False:
            with self.session:
                chat = Chat(
                user_id_1=user_id_1_,
                user_id_2=user_id_2_,
                )
                self.session.add_all([chat])
                self.session.commit()
                return True
        return False

    def search_chat_id(self,user_id_1,user_id_2):
        try:
            chat = self.session.query(Chat).filter(Chat.user_id_1 == user_id_1 and Chat.user_id_2==user_id_2 ).one()
            return chat.chat_id
        except:
            try:
                chat = self.session.query(Chat).filter(Chat.user_id_1 == user_id_2 and Chat.user_id_2==user_id_1 ).one()
                return chat.chat_id
            except:
                return False
               
    def delete_chat(self,user_id_1,user_id_2):
        chat_id = self.search_chat_id(user_id_1,user_id_2)
        if chat_id is not False:
            # Elimina todos los sms del chat
            for id in self.session.query(Messenger).filter(Messenger.chat_id==chat_id).all():
                self.session.delete(id)
            
            contain = self.session.query(Chat).get(chat_id)
            self.session.delete(contain) 
            self.session.commit()
            return True
        return False

    def search_chat(self,user_id_1,user_id_2):
        chat_id = self.search_chat_id(user_id_1,user_id_2)
        if chat_id is not False:
            try:
                result = self.session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.chat_id==chat_id).all()
                return result
            except:
                return []