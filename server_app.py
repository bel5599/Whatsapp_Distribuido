if __name__ == "__main__":
    import asyncio
    import threading
    import time
    from typer import Typer
    from fastapi import FastAPI, Request
    from uvicorn import Config, Server

    # using this imports until node submodule is implemented
    from server.chord.node import Node
    from server.chord.remote_node import RemoteNode
    from server.util import generate_id
    from server.chord.routers import fingers, predecessor, successor, debug as debug_module

    from shared import get_ip, LOCAL_IP

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

    @fastapi_app.get("/heart")
    def ping():
        return "beat"

    @typer_app.command()
    def up(capacity: int = 64, port: str = "4173", local: bool = False, debug: bool = False, stabilize: bool = True, interval: int = 5):
        if debug:
            fastapi_app.include_router(debug_module.router)

        capacity = min(capacity, 256)

        ip = get_ip(local)
        node = Node.create_network(ip, port, capacity)

        inject_node(fastapi_app, node)

        def _stabilize():
            if stabilize:
                time.sleep(1)
                node.stabilize(interval)
        stabilize_task = threading.Thread(target=_stabilize)

        config = Config(fastapi_app, host=ip, port=int(port))
        server = Server(config)

        stabilize_task.start()
        asyncio.run(server.serve())

    @typer_app.command()
    def join(address: str, port: str = "4173", local: bool = False, debug: bool = False, stabilize: bool = True, interval: int = 5):
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

        ip = get_ip(local)
        node = Node(ip, port, capacity)

        remote_node.id = generate_id(f"{remote_ip}:{remote_port}", capacity)
        remote_node.set_local_node(node)

        inject_node(fastapi_app, node)

        def _join_network():
            time.sleep(1)
            node.join_network(remote_node)
            if stabilize:
                node.stabilize(interval)
        join_task = threading.Thread(target=_join_network)

        config = Config(fastapi_app, host=ip, port=int(port))
        server = Server(config)

        join_task.start()
        asyncio.run(server.serve())

    typer_app()
