from time import sleep

from ..requests import RequestManager


class HeartBeatManager:
    def __init__(self):
        self.request_manager_list = []

    def add_request_manager(self, request_manager: RequestManager):
        self.request_manager_list.append(request_manager)

    def check_health(self, interval: int):
        while True:
            for request_manager in self.request_manager_list:
                request_manager.get("/beat")

            sleep(interval)
