# levanta la interfaz del cliente
if __name__ == "__main__":
    import uvicorn
    from typer import Typer
    from client.client import service
    from shared import get_ip, SERVICE_PORT

    typer_app = Typer()

    @typer_app.command()
    def run():
        ip = get_ip()
        uvicorn.run(service, host=ip, port=int(SERVICE_PORT))

    typer_app()
