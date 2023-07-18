# levanta la interfaz del cliente
if __name__ == "__main__":
    import json
    from uvicorn import Config, Server
    from threading import Thread
    import time
    import asyncio
    from typer import Typer

    from client.client import client_interface, client, service
    from client.utils import SERVER_ADDRESSES_CACHE_FILENAME
    from shared import LOCAL_IP, CLIENT_PORT, SERVER_PORT, inject_to_state, get_ip
    from server.util import generate_id
    from server.node.remote_entity_node import RemoteEntityNode
    from server.chord.base_node import BaseNodeModel
    from service.broadcast.server import broadcast_task

    # handle shutdown
    client_interface.on_event("shutdown")(client.save_nodes)

    typer_app = Typer()

    @typer_app.command()
    def run():
        inject_to_state(client_interface, "client", client)
        inject_to_state(service, "client", client)

        nodes: list[RemoteEntityNode] = []

        ip_addresses = broadcast_task(
            timeout=5, limit=10, message_count=5, from_client=True)
        if len(ip_addresses):
            first = RemoteEntityNode(-1, ip_addresses[0], SERVER_PORT)
            try:
                capacity = first.network_capacity()
            except:
                pass
            else:
                # add nodes from broadcast
                nodes.extend([RemoteEntityNode(generate_id(
                    f"{ip}:{SERVER_PORT}", capacity), ip, SERVER_PORT) for ip in ip_addresses])

        # load nodes from cache
        try:
            servers: list[dict] = []
            with open(SERVER_ADDRESSES_CACHE_FILENAME, "r") as j:
                servers = json.load(j)
        except:
            pass
        else:
            if len(servers):
                nodes.extend([RemoteEntityNode.from_base_model(
                    BaseNodeModel(**n)) for n in servers])

        # add nodes to client manager
        client.manager.add_nodes(*nodes)

        if len(client.manager.get_nodes()) == 0:
            raise Exception(
                "Unable to find a server node to connect! Try again.")

        def _service_task():
            config = Config(service, host=get_ip(), port=int(CLIENT_PORT))
            server = Server(config)
            asyncio.run(server.serve())
        service_task = Thread(target=_service_task, daemon=True)

        def update():
            time.sleep(1)
            client.update_servers()
        stabilize_task = Thread(target=update, daemon=True)

        config = Config(client_interface, host=LOCAL_IP, port=int(CLIENT_PORT))
        server = Server(config)

        service_task.start()
        stabilize_task.start()
        asyncio.run(server.serve())

    typer_app()
