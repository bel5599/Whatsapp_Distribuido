from time import sleep

from ..requests import RequestManager


class HeartBeatManager:
    def __init__(self):
        self.request_manager_list = set()

    def add_request_manager(self, request_manager: RequestManager):
        self.request_manager_list.add(request_manager)

    def check_health(self, interval: int):
        while True:
            for request_manager in self.request_manager_list:
                try:
                    response = request_manager.get("/heart")
                except:
                    self.request_manager_list.remove(request_manager)
                else:
                    if not response.status_code == 200:
                        self.request_manager_list.remove(request_manager)

            sleep(interval)

# TODO:
# 1- request_manager_list sea un set de python
# 2- en lugar de hacer el for y ya, necesito que
# cojas todas los request manager que:
#   1- o dieron status_code != 200
#   2- o dieron error
# asumes q esos nodos se desconectaron y por tanto
# remuevelos de la lista (que seria un set)
# aqui tienes la documentacion de los set https://docs.python.org/3.9/library/stdtypes.html#set
# ;)
