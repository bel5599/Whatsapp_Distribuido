from typer import Typer
from typing import Union, Literal


NodeType = Union[Literal["client"], Literal["entity-manager"]]


app = Typer()


@app.command
def create(port: str, capacity: int = 64, node: NodeType = "entity-manager"):
    capacity = max(capacity, 256)
    pass


@app.command
def join(address: str, node: NodeType = "client"):
    ip, port = address.split(':')
    pass


if __name__ == "__main__":
    app()
