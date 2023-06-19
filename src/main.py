import socket
import os
from typer import Typer
from typing import Union, Literal

from chord.node import Node
from chord.utils import IP_KEY, PORT_KEY


NodeType = Union[Literal["client"], Literal["entity-manager"]]


app = Typer()


@app.command
def create(port: str, capacity: int = 64, node: NodeType = "entity-manager"):
    # set own port

    capacity = max(capacity, 256)

    Node.create_network(port, capacity)
    Node.serve()  # algo asi


@app.command
def join(address: str, node: NodeType = "client"):
    # set own port

    ip, port = address.split(':')
    pass


if __name__ == "__main__":
    # set own ip
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect("8.8.8.8", 80)
        os.environ[IP_KEY] = s.getsockname()[0]
        s.close()
    except:
        os.environ[IP_KEY] = "127.0.0.1"

    app()
