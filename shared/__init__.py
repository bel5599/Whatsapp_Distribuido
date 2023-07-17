import socket
from fastapi import FastAPI, Request


LOCAL_IP = "127.0.0.1"
SERVICE_PORT = "8480"
CLIENT_PORT = "9050"
SERVER_PORT = "4173"

HEART_RESPONSE = "beat"


def get_ip(local=False):
    ip = ""

    if local:
        ip = LOCAL_IP
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except:
            ip = LOCAL_IP

    return ip


def inject_to_state(app: FastAPI, name: str, obj):
    async def middleware(request: Request, call_next):
        setattr(request.state, name, obj)
        return await call_next(request)

    app.middleware("http")(middleware)
