from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_client import*


class DataBaseClient:
    def __init__(self,name:str = 'client_data'):
        engine = create_engine('sqlite:///'+name+'.sqlite')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    # Contacts
    # Devuelve una lista:Contacts de todos los usuarios en la base datos
    def get_contacts(self):
        try:
            contacts = self.session.query(Contacts).filter(Contacts.name!="Unknown").all()
            return contacts
        except:
            return False
        
    def add_contacts(self,nickname_:str,name_:str = "Unknown"):
        try:
            with self.session:
                contact = Contacts(
                nickname=nickname_,
                name = name_)
                self.session.add_all([contact])
                self.session.commit()
                return True
        except:
            return False
    
    def update_contact(self,nickname:str,name:str):
        self.session.query(Contacts).filter(Contacts.nickname == nickname).update({Contacts.name: name})
        self.session.commit()
        
    def contain_contact(self,nickname_:str):
        contain = self.session.query(Contacts).get(nickname_)
        return contain is not None 
                           
    def delete_contact(self,nickname:str):
        contain = self.session.query(Contacts).get(nickname)
        if contain is not None:
            self.session.delete(contain) 
            self.session.commit()
            return True
        return False

    def get_name(self,nickname:str):
        name = self.session.query(Contacts.name).filter(Contacts.nickname==nickname).one()
        return name[0]
    
    def get_nickname(self,name:str):
        nickname = self.session.query(Contacts.nickname).filter(Contacts.name==name).one()
        return nickname[0]
    
        
    # MESSENGER
    def get_messages(self):
        try:
            users = self.session.query(Messenge).all()
            return users
        except:
            return False
        
    def add_messenges(self,source:str,destiny:str,value_:str,id:int = -1):
        # Crear el chat si no existe y luego agregarselo a la tabla 
        self.add_chat(source,destiny)    
        idChat = self.search_chat_id(source,destiny)
        try:
            with self.session:
                if id!=-1:
                    messenger = Messenge(
                    messenger_id = id,        
                    user_id_from= source,
                    user_id_to  = destiny,   
                    chat_id     = idChat,      
                    value       = value_,  )    
                else:
                    messenger = Messenge(
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
        
    def delete_messenges(self,id_messenge:int):
        messenge = self.session.query(Messenge).get(id_messenge)
        if messenge is not None:
            self.session.delete(messenge) 
            self.session.commit()
            return True
        return False

    # Todos los sms que envie, o que envie a user
    # Devuelve una lista de tuplas(user_from,Value)
    def search_messenges_from(self,me:str, user:str = None):
        try:
            if user is None:
                result = self.session.query(Messenge.user_id_from,Messenge.value).filter(Messenge.user_id_from == me).all()
            else:
                result = self.session.query(Messenge.user_id_from,Messenge.value).filter(Messenge.user_id_from == me and Messenge.user_id_to == user).all()
            
            return result
        except:
            return []    

    # Todos los sms que me enviaron , o los que me envio user
    # Devuelve una lista de tuplas(user_from,Value)
    def search_messenges_to(self,me:str,user:str=None):
        try:
            if user is None:
                result = self.session.query(Messenge.user_id_from,Messenge.value).filter(Messenge.user_id_to == me).all()       
            else:
                result = self.session.query(Messenge.user_id_from,Messenge.value).filter(Messenge.user_id_from == user and Messenge.user_id_to == me).all()
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
            for id in self.session.query(Messenge).filter(Messenge.chat_id==chat_id).all():
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
                result = self.session.query(Messenge.user_id_from,Messenge.value).filter(Messenge.chat_id==chat_id).all()
                return result
            except:
                return []
