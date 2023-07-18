import asyncio
from threading import Thread
import time
import socket
from fastapi import FastAPI, Request
from uvicorn import Config, Server

from shared import inject_to_state, get_ip
from . import BROADCAST_IP, BROADCAST_PORT, BROADCAST_MESSAGE, BROADCAST_SERVER_PORT


class IPBox:
    def __init__(self):
        self.ips: list[str] = []

    def add(self, ip: str):
        self.ips.append(ip)


def broadcast_task(timeout: float = 5, limit: int = 10):
    # prepare app

    app = FastAPI()
    ip_box = IPBox()

    inject_to_state(app, "ip_box", ip_box)

    def find(request: Request):
        ip_box: IPBox = request.state.ip_box
        client = request.client
        if client and len(ip_box.ips) < limit:
            ip_box.add(client.host)

    app.get("/find")(find)

    def _app_task():
        config = Config(app, host=get_ip(), port=int(BROADCAST_SERVER_PORT))
        server = Server(config)
        asyncio.run(server.serve())
    app_task = Thread(target=_app_task, daemon=True)

    # prepare broadcast socket

    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # server_socket.settimeout(0.2)

    def _socket_task():
        while True:
            server_socket.sendto(
                BROADCAST_MESSAGE, (BROADCAST_IP, int(BROADCAST_PORT)))
            time.sleep(0.1)
    socket_task = Thread(target=_socket_task, daemon=True)

    # prepare task

    def task():
        app_task.start()
        socket_task.start()

        app_task.join(timeout)
        socket_task.join(timeout)

        return ip_box

    return task
