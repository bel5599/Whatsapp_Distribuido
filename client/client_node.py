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
        