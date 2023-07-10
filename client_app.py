
# levanta la interfaz del cliente
if __name__ == "__main__":
    import uvicorn
    import threading
    import time
    from typer import Typer
    from client.client import client_interface,client

    typer_app = Typer()

    @typer_app.command()
    def run(ip:str,port:str ='9000'):
        client.ip = ip
        client.port = port
        # Creacion de un hilo para este servicio
        def update():
            time.sleep(1)
            client.update_servers()
        stabilize_task = threading.Thread(target=update)    
        # Levantar el hilo
        stabilize_task.start()
        # Correr el cliente
        uvicorn.run(client_interface,host=ip, port=int(port))
        
    typer_app()