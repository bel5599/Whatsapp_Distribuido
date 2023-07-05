from service.heartbeat import HeartBeatManager
from service.requests import RequestManager

class ClientNode:
    def __init__(self):
        self.user = {}
        self.login = False
        self.manager =  HeartBeatManager()

    def login_user(self, nickname: str, password: str, server: list):
        self.user['nickname'] = nickname
        self.user['password'] = password
        self.login = True
        for s in server:
            ip,port = s.split(':')
            self.manager.add_request_manager(RequestManager(ip,port))
    
    def server_list(self):
        return list(self.manager.request_manager_list)
        
    def logout_user(self):
        self.user = {}
        self.server = []
        self.login = False
    
    def update_servers(self):
        self.manager.check_health(3)
        
            