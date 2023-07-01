from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from ..entity_node import EntityNode


class ChatModel(BaseModel):
    user_1: str
    user_2: str


router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/")
def search_chat_id(model: ChatModel, request: Request):
    node: EntityNode = request.state.node

    try:
        chat_id = node.search_chat_id(model.user_1, model.user_2)
    except:
        raise HTTPException(status_code=404, detail="chat id not found!")
    else:
        return node.serialize()#tengo que arreglarlo


@router.put("/add")
def add_chat(model: ChatModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.add_chat(model.user_1, model.user_2)
    except:
        raise HTTPException(
            status_code=500, detail="add chat failed!")
    else:
        return {"success": result}


@router.delete("/delete/{model.user_1}{model.user_2}")
def delete_chat(model: ChatModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_chat(model.user_1, model.user_2)
    except:
        raise HTTPException(
            status_code=500, detail="delete chat failed!")
    else:
        return {"success": result}
