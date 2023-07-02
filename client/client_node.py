class ClientNode:
    def __init__(self):
        self.user = {}
        self.server = []  # lista de ip:port
        self.login = False

    def login_user(self, nickname: str, password: str, server: list):
        self.user['nickname'] = nickname
        self.user['password'] = password
        self.login = True
        for s in server:
            self.server.append(s)
    
    def logout_user(self):
        self.user = {}
        self.server = []
        self.login = False
        
        
    # def check_password(self,nickname:str,password:str):
    #     if self.user['nickname'] == nickname and self.user['password'] == password:
    #         return True
    #     return False

    # def check_login(self,nickname:str,password:str):
    #     if self.check_password(nickname,password):
    #         return self.login
