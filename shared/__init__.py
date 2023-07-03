import socket


LOCAL_IP = "127.0.0.1"


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
