import socket


LOCAL_IP = "127.0.0.1"

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
