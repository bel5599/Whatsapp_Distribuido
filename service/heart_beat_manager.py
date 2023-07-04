from .requests import RequestManager

class HeartBeatManager:
    def __init__(self):
        self.request_manager_list = []

    def add_request_manager(self, request_manager):
        self.request_manager_list.append(request_manager)

    def check_health(self):
        for request_manager in self.request_manager_list:
            request_manager.get("/beat")
    
