
# levanta la interfaz del cliente
if __name__ == "__main__":
    import uvicorn
    from typer import Typer
    from shared import get_ip
    from client.client import client_interface,client

    typer_app = Typer()

    @typer_app.command()
    def run(ip:str,port:int =9000):
        uvicorn.run(client_interface,host=ip, port=port)
        client.update_servers()

    typer_app()