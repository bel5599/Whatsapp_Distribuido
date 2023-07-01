if __name__ == "__main__":
    import asyncio
    from logging import basicConfig, DEBUG
    from typer import Typer, Argument
    from fastapi import FastAPI, Request
    from uvicorn import Config, Server

    # using this imports until node submodule is implemented
    from server.chord.node import Node
    from server.chord.remote_node import RemoteNode
    from server.util import generate_id, get_ip, LOCAL_IP
    from server.chord.routers import fingers, predecessor, successor

    basicConfig(level=DEBUG)

    def inject_node(app: FastAPI, node: Node):
        async def middleware(request: Request, call_next):
            request.state.node = node
            return await call_next(request)

        app.middleware("http")(middleware)

    typer_app = Typer()

    fastapi_app = FastAPI()
    fastapi_app.include_router(fingers.router)
    fastapi_app.include_router(successor.router)
    fastapi_app.include_router(predecessor.router)

    @typer_app.command()
    def create(capacity: int = Argument(64), port: str = "4173", local: bool = False):
        capacity = min(capacity, 256)

        ip = get_ip(local)
        node = Node.create_network(ip, port, capacity)

        inject_node(fastapi_app, node)

        config = Config(fastapi_app, host=ip, port=int(port))
        server = Server(config)
        asyncio.run(server.serve())

    @typer_app.command()
    def join(address: str, port: str = "4173", local: bool = False):
        if not local:
            remote_ip, remote_port = address.split(
                ":")
        else:
            remote_ip = LOCAL_IP
            remote_port = address

        remote_node = RemoteNode(-1, remote_ip, remote_port)

        capacity = remote_node.network_capacity()

        remote_node.id = generate_id(f"{remote_ip}:{remote_port}", capacity)

        ip = get_ip(local)
        node = Node(ip, port, capacity)

        inject_node(fastapi_app, node)

        config = Config(fastapi_app, host=ip, port=int(port))
        server = Server(config)
        asyncio.run(server.serve())

        node.join_network(remote_node)

    typer_app()
