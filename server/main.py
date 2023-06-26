if __name__ == "__main__":
    import asyncio
    from typer import Typer
    from fastapi import FastAPI, Request
    from uvicorn import Config, Server

    # using this imports until node submodule is implemented
    from .chord.node import Node
    from .chord.remote_node import RemoteNode
    from .util import generate_id, get_ip

    def inject_node(app: FastAPI, node: Node):
        @app.middleware("http")
        async def middleware(request: Request, call_next):
            request.state.node = node

            return await call_next(request)

    typer_app = Typer()
    fastapi_app = FastAPI()

    @typer_app.command()
    def create(capacity: int = 64, port: str = "4173"):
        capacity = min(capacity, 256)

        ip = get_ip()
        node = Node.create_network(ip, port, capacity)

        inject_node(fastapi_app, node)

        config = Config("main:fastapi_app", host=ip, port=int(port))
        server = Server(config)
        asyncio.run(server.serve())

    @typer_app.command()
    def join(address: str, port: str = "4173"):
        remote_ip, remote_port = address.split(":")
        remote_node = RemoteNode(-1, remote_ip, remote_port)

        capacity = remote_node.network_capacity()

        remote_node.id = generate_id(address, capacity)

        ip = get_ip()
        node = Node(generate_id(f"{ip}:{port}", capacity), ip, port)
        inject_node(fastapi_app, node)

        config = Config("main:fastapi_app", host=ip, port=int(port))
        server = Server(config)
        asyncio.run(server.serve())

        node.join_network(remote_node)
