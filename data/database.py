from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import*



class DataBase:
    def __init__(self,name:str = 'data'):
        engine = create_engine('sqlite:///'+name+'.sqlite')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    # USER 
    #Devuelve una lista:user de todos los usuarios de la base datos 
    def get_users(self):
        try:
            users = self.session.query(User).all()
            return users
        except:
            return False
        
    def add_user(self,nickname_:str,password_:str):
        try:
            with self.session:
                user = User(
                nickname=nickname_,
                password = password_)
                self.session.add_all([user])
                self.session.commit()
                return True
        except:
            return False
        
    def contain_user(self,nickname_:str):
        contain = self.session.query(User).get(nickname_)
        return contain is not None 
                           
    def delete_user(self,nickname:str):
        contain = self.session.query(User).get(nickname)
        if contain is not None:
            self.session.delete(contain) 
            self.session.commit()
            return True
        return False

    def get_password(self,nickname:str):
        password = self.session.query(User.password).filter(User.nickname==nickname).one()
        return password[0]
    
    # MESSENGER
    def get_messages(self):
        try:
            users = self.session.query(Messenger).all()
            return users
        except:
            return False
        
    def add_messenger(self,source:str,destiny:str,value_:str,id:int = -1):
        # Crear el chat si no existe y luego agregarselo a la tabla 
        self.add_chat(source,destiny)    
        idChat = self.search_chat_id(source,destiny)
        try:
            with self.session:
                if id!=-1:
                    messenger = Messenger(
                    messenger_id = id,        
                    user_id_from= source,
                    user_id_to  = destiny,   
                    chat_id     = idChat,      
                    value       = value_,  )    
                else:
                    messenger = Messenger(
                    user_id_from= source,
                    user_id_to  = destiny,   
                    chat_id     = idChat,      
                    value       = value_,  )    
            
                self.session.add_all([messenger])
                self.session.commit()
                return True
        except:
            return False
                   
        # Se podria coger la fecha y hora de la computadora en el momento que se usa el m\'etodo
        
    def delete_messenger(self,id_messenger:int):
        messenger = self.session.query(Messenger).get(id_messenger)
        if messenger is not None:
            self.session.delete(messenger) 
            self.session.commit()
            return True
        return False

    # Todos los sms que envie, o que envie a user
    # Devuelve una lista de tuplas(user_from,Value)
    def search_messenger_from(self,me:str, user:str = None):
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
    def search_messenger_to(self,me:str,user:str=None):
        try:
            if user is None:
                result = self.session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_to == me).all()       
            else:
                result = self.session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.user_id_from == user and Messenger.user_id_to == me).all()
                return result
        except:
            return []   
    
    # CHAT
    def add_chat(self,user_id_1_:str,user_id_2_:str):
        #if  self.search_chat_id(user_id_1_,user_id_2_) is False:
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

    def search_chat_id(self,user_id_1:str,user_id_2:str):
        try:
            chat = self.session.query(Chat).filter(Chat.user_id_1 == user_id_1 and Chat.user_id_2==user_id_2 ).one()
            return chat.chat_id
        except:
            try:
                chat = self.session.query(Chat).filter(Chat.user_id_1 == user_id_2 and Chat.user_id_2==user_id_1 ).one()
                return chat.chat_id
            except:
                return False
               
    def delete_chat(self,user_id_1:str,user_id_2:str):
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

    def search_chat(self,user_id_1:str,user_id_2:str):
        chat_id = self.search_chat_id(user_id_1,user_id_2)
        if chat_id is not False:
            try:
                result = self.session.query(Messenger.user_id_from,Messenger.value).filter(Messenger.chat_id==chat_id).all()
                return result
            except:
                return []
    
    # copia los datos de la base datos source para self
    def copy_database(self,source):
        list_new_users =[]
        # copiar los usuarios de origen para destino que no tiene
        list_users = source.get_users()
        for user in list_users:
            if self.add_user(user.nickname,user.password):
                list_new_users.append(user.nickname)
            
        # copiar los mensajes de origen para destino que no tiene
        list_messenges = source.get_messages()
        for messenge in list_messenges:
            if list_new_users.count(messenge.user_id_from) or list_new_users.count(messenge.user_id_to):
                self.add_messenger(messenge.user_id_from,messenge.user_id_to,messenge.value)
        
        # copiar los chats de origen para destino que no tiene