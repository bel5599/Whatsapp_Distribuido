if __name__ == "__main__":
    import asyncio
    import threading
    import time
    from typer import Typer
    from fastapi import FastAPI, Request
    from uvicorn import Config, Server

    # using this imports until node submodule is implemented

    # from server.chord.node import Node
    # from server.chord.remote_node import RemoteNode
    from server.node.entity_node import EntityNode as Node
    from server.node.remote_entity_node import RemoteEntityNode as RemoteNode

    from server.util import generate_id
    from server.chord.routers import router as chord_router, debug_router
    from server.node.routers import router as entity_router

    from shared import get_ip, LOCAL_IP

    def inject_node(app: FastAPI, node: Node):
        async def middleware(request: Request, call_next):
            request.state.node = node
            return await call_next(request)

        app.middleware("http")(middleware)

    typer_app = Typer()

    fastapi_app = FastAPI()
    fastapi_app.include_router(chord_router)
    fastapi_app.include_router(entity_router)

    @typer_app.command()
    def up(capacity: int = 64, port: str = "4173", local: bool = False, debug: bool = False, interval: float = 0.3):
        if debug:
            fastapi_app.include_router(debug_router)

        capacity = min(capacity, 256)

        ip = get_ip(local)
        node = Node.create_network(ip, port, capacity)

        inject_node(fastapi_app, node)

        healthy_task = threading.Thread(
            target=node.keep_healthy, args=(interval, node.update_replications), daemon=True)

        config = Config(fastapi_app, host=ip, port=int(port))
        server = Server(config)

        healthy_task.start()
        asyncio.run(server.serve())

    @typer_app.command()
    def join(address: str, port: str = "4173", local: bool = False, debug: bool = False, interval: float = 0.3):
        if debug:
            fastapi_app.include_router(debug_router)

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

        def join_network():
            time.sleep(1)
            node.join_network(remote_node)
            node.keep_healthy(interval, node.update_replications)
        join_task = threading.Thread(target=join_network, daemon=True)

        config = Config(fastapi_app, host=ip, port=int(port))
        server = Server(config)

        join_task.start()
        asyncio.run(server.serve())

    typer_app()
