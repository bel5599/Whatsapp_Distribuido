# levanta la interfaz del cliente
if __name__ == "__main__":
    import json
    import uvicorn
    import threading
    import time
    from typer import Typer
    from client.client import client_interface, client
    from client.utils import SERVER_ADDRESSES_CACHE_FILENAME
    from shared import LOCAL_IP, CLIENT_PORT, SERVER_PORT
    from server.util import generate_id
    from server.node.remote_entity_node import RemoteEntityNode
    from server.chord.base_node import BaseNodeModel

    # handle shutdown
    client_interface.on_event("shutdown")(client.save_nodes)

    typer_app = Typer()

    @typer_app.command()
    def run(ip: str):
        server_node = RemoteEntityNode(-1, ip, SERVER_PORT)
        capacity = server_node.network_capacity()
        server_node.id = generate_id(
            f"{server_node.ip}:{server_node.port}", capacity)
        servers: list[dict] = []

        try:
            with open(SERVER_ADDRESSES_CACHE_FILENAME, "r") as j:
                servers = json.load(j)
        except:
            pass
        if len(servers):
            nodes = [RemoteEntityNode.from_base_model(
                BaseNodeModel(**n)) for n in servers]
        else:
            nodes = server_node.all_nodes()

        client.manager.add_nodes(*nodes)

        # Creacion de un hilo para este servicio

        def update():
            time.sleep(1)
            client.update_servers()
        stabilize_task = threading.Thread(target=update, daemon=True)
        # Levantar el hilo
        stabilize_task.start()
        # Correr el cliente
        uvicorn.run(client_interface, host=LOCAL_IP, port=int(CLIENT_PORT))

    typer_app()
