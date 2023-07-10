# levanta la interfaz del cliente
if __name__ == "__main__":
    import uvicorn
    import threading
    import time
    from typer import Typer
    from client.client import service

    typer_app = Typer()

    @typer_app.command()
    def run(ip:str):
        uvicorn.run(service,host=ip, port=int('8765'))

    typer_app()