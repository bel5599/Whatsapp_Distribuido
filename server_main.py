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
    from server.chord.routers import fingers, predecessor, successor, debug as debug_module

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
    def create(capacity: int = Argument(64), port: str = "4173", local: bool = False, debug: bool = False):
        if debug:
            fastapi_app.include_router(debug_module.router)

        capacity = min(capacity, 256)

        ip = get_ip(local)
        node = Node.create_network(ip, port, capacity)

        inject_node(fastapi_app, node)

        config = Config(fastapi_app, host=ip, port=int(port))
        server = Server(config)
        asyncio.run(server.serve())

    @typer_app.command()
    def join(address: str, port: str = "4173", local: bool = False, debug: bool = False):
        if debug:
            fastapi_app.include_router(debug_module.router)

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

        async def _join_network():
            await asyncio.sleep(1)
            node.join_network(remote_node)

        async def _serve():
            config = Config(fastapi_app, host=ip, port=int(port))
            server = Server(config)
            await server.serve()

        async def _gather():
            s = _serve()
            j = _join_network()
            await asyncio.gather(s, j)

        asyncio.run(_gather())

    typer_app()
