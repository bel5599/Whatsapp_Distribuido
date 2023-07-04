if __name__ == "__main__":
    import asyncio
    from typer import Typer
    from uvicorn import Config, Server
    import time

    from service.heartbeat.app import app as fastapi_app, manager
    from shared import get_ip

    typer_app = Typer()

    @typer_app.command()
    def up(port: str = "4173", interval: int = 10, local: bool = False):
        ip = get_ip(local)

        async def _serve():
            config = Config(fastapi_app, host=ip, port=int(port))
            server = Server(config)
            await server.serve()

        async def _start_service():
            await asyncio.sleep(1)
            # manager hace algo para empezar a avisar
            # cada cierto tiempo (usar interval)
            manager.check_health()
            time.sleep(interval)

        async def _gather():
            s = _serve()
            h = _start_service()
            await asyncio.gather(s, h)

        asyncio.run(_gather())

    typer_app()
