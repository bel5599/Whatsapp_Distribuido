# levanta la interfaz del cliente
if __name__ == "__main__":
    import uvicorn
    import threading
    import time
    from typer import Typer
    from client.client import client_interface, client
    from shared import LOCAL_IP, CLIENT_PORT

    typer_app = Typer()

    @typer_app.command()
    def run(ip: str):
        client.insert_servers()
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
