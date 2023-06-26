from fastapi import APIRouter, Request, HTTPException

# from ..base_node import BaseNodeModel
from ..entity_node import EntityNode
from pydantic import BaseModel
# from ..remote_node import RemoteNode

class MessengerModel(BaseModel):
    source: str
    destiny: str
    value: str


router = APIRouter(prefix="/messenger", tags=["messenger"])

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
            status_code=500, detail="delete user failed!")
    else:
        return {str(result): result}