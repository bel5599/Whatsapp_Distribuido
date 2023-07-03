from fastapi import FastAPI, Request

from . import HeartBeatManager
from server.chord.base_node import BaseNode, BaseNodeModel


app = FastAPI()
manager = HeartBeatManager()


async def middleware(request: Request, call_next):
    request.state.manager = manager
    return await call_next(request)

app.middleware("http")(middleware)


@app.post("/register")
def register_node(model: BaseNodeModel, request: Request):
    manager: HeartBeatManager = request.state.manager

    # registrar nodo en el manager
    pass