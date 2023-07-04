from fastapi import FastAPI, Request

from . import HeartBeatManager
from ..requests import RequestManager
from server.chord.base_node import BaseNodeModel


app = FastAPI()
manager = HeartBeatManager()


async def middleware(request: Request, call_next):
    request.state.manager = manager
    return await call_next(request)

app.middleware("http")(middleware)


@app.post("/register")
def register_node(model: BaseNodeModel, request: Request):
    manager: HeartBeatManager = request.state.manager

    request_manager = RequestManager(model.ip, model.port)
    manager.add_request_manager(request_manager)
