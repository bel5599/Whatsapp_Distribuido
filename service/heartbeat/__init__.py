from time import sleep

from ..requests import RequestManager


class HeartBeatManager:
    def __init__(self):
        self.request_manager_list = set()

    def add_request_manager(self, request_manager: RequestManager):
        self.request_manager_list.add(request_manager)

    def check_health(self, interval: int):
        while True:
            temp_set = set()
            for request_manager in self.request_manager_list:
                try:
                    response = request_manager.get("/chord/heart")
                except:
                    temp_set.add(request_manager)
                else:
                    if response.status_code != 200:
                        temp_set.add(request_manager)

            self.request_manager_list = self.request_manager_list - temp_set

            sleep(interval)
