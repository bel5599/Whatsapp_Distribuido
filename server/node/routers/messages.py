from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode
from ..models import MessagesModel, SearchMessagesModel, DataBaseModel


router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/to")
def search_messages_to(model: SearchMessagesModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_messages_to(
            model.destiny, model.database_id)
    except:
        raise HTTPException(status_code=404, detail="messages not found!")
    else:
        return [{"user_id_from": user_id_from, "value": value} for (user_id_from, value) in result]


@router.put("/add")
def add_messages(model: MessagesModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.add_messages(
            model.source, model.destiny, model.value, model.database_id,model.id)
    except:
        raise HTTPException(
            status_code=500, detail="add messages failed!")
    else:
        return {"success": result}


@router.delete("/delete/to/{me}")
def delete_messages_to(me: str, model: DataBaseModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_messages_to(me, model.database_id)
    except:
        raise HTTPException(
            status_code=500, detail="delete messages failed!")
    else:
        return {"success": result}
