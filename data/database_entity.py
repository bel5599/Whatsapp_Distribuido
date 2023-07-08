from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_entity import*

class DataBaseUser:
    def __init__(self,name:str = 'user_data'):
        engine = create_engine('sqlite:///'+name+'.sqlite')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    # USER 
    # Devuelve una lista:user de todos los usuarios de la base datos 
    def get_users(self):
        try:
            users = self.session.query(User).all()
            return users
        except:
            return False
        
    def add_user(self,nickname_:str,password_:str,ip_:str,port_:str):
        try:
            with self.session:
                user = User(
                nickname=nickname_,
                password = password_,
                ip = ip_,
                port = port_
                )
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
    
    def update_user(self,nickname:str,ip:str,port:str):
        self.session.query(User).filter(User.nickname == nickname).update({User.ip:ip,User.port:port})
        self.session.commit()
    
    def get_ip_port(self,nickname:str):
        password = self.session.query(User.ip,User.port).filter(User.nickname==nickname).one()
        return password[0]+password[1]

    # MESSENGES
    def get_messages(self):
        try:
            users = self.session.query(Messenge).all()
            return users
        except:
            return False
        
    def add_messenges(self,source:str,destiny:str,value_:str):
        # Crear el chat si no existe y luego agregarselo a la tabla 
        try:
            with self.session:
                messenger = Messenge(
                    user_id_from= source,
                    user_id_to  = destiny,     
                    value       = value_,  
                )    
                self.session.add_all([messenger])
                self.session.commit()
                return True
        except:
            return False
                   
        # Se podria coger la fecha y hora de la computadora en el momento que se usa el m\'etodo
        
    def delete_messenges(self,id_messenge:int):
        messenger = self.session.query(Messenge).get(id_messenge)
        if messenger is not None:
            self.session.delete(messenger) 
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
        
        # copiar los chats de origen para destino que no tiene# copia los datos de la base datos source para self            