from hashlib import sha256
from os import environ

PORT_KEY = "REQUESTER_PORT"
IP_KEY = "REQUESTER_IP"


def generate_id(text: str, bits=64):
    return int(sha256(text.encode()).hexdigest(), 16) % 2**bits


def get_requester():
    # si no hay internet, obtener el port de otra forma
    ip = environ.get(IP_KEY)
    port = environ.get(PORT_KEY)
    return [ip, port]
