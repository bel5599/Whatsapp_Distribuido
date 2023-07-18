import socket
from threading import Thread

from . import BROADCAST_PORT, BROADCAST_SERVER, BROADCAST_CLIENT
from service.requests import RequestManager


def client_broadcast_task():
    client = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client.bind(("", int(BROADCAST_PORT)))

    def _socket_task():
        while True:
            data, addr = client.recvfrom(1024)
            if data == BROADCAST_SERVER[1]:
                request_manager = RequestManager(
                    addr[0], BROADCAST_SERVER[0])
                try:
                    request_manager.get("/find")
                except:
                    pass
            elif data == BROADCAST_CLIENT[1]:
                request_manager = RequestManager(
                    addr[0], BROADCAST_CLIENT[0])
                try:
                    request_manager.get("/find")
                except:
                    pass

    socket_task = Thread(target=_socket_task, daemon=True)

    socket_task.start()
