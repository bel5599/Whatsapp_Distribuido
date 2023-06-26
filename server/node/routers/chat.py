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