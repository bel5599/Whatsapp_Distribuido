from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode
from pydantic import BaseModel

class MessengerModel(BaseModel):
    source: str
    destiny: str
    value: str


router = APIRouter(prefix="/messenger", tags=["messenger"])

@router.get("/from")
def search_messenger_from(me, user, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_messenger_from(me, user)
    except:
        raise HTTPException(status_code=404, detail="messenges not found!")
    else:
        return {str(result): result}
    
@router.get("/to")
def search_messenger_to(me, user, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_messenger_to(me, user)
    except:
        raise HTTPException(status_code=404, detail="messenges not found!")
    else:
        return {str(result): result}

@router.put("/add")
def add_messenger(model: MessengerModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.add_messenger(model.source, model.destiny, model.value)
    except:
        raise HTTPException(
            status_code=500, detail="add messenger failed!")
    else:
        return {str(result): result}
    
@router.delete("/delete/{id}")
def delete_messenger(id: int, request: Request):
    node:EntityNode = request.state.node

    try:
        result = node.delete_messenger(id)
    except:
        raise HTTPException(
            status_code=500, detail="delete messenger failed!")
    else:
        return {str(result): result}
    
