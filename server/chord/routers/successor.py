from fastapi import APIRouter, Request, HTTPException

from ..base_node import BaseNodeModel
from ..node import Node
from ..remote_node import RemoteNode


router = APIRouter(prefix="/successor")


@router.get("/")
def get_successor(request: Request):
    node: Node = request.state.node

    successor = node.successor()
    if successor:
        return successor.serialize()

    raise HTTPException(status_code=404, detail="successor not found!")


@router.put("/")
def set_successor(model: BaseNodeModel, request: Request):
    node: Node = request.state.node

    try:
        new_node = RemoteNode.from_base_model(model)
        node.set_successor(new_node)
    except:
        raise HTTPException(
            status_code=500, detail="setting successor failed!")
    else:
        return node.serialize()


@router.get("/{id}")
def find_successor(id: int, request: Request):
    node: Node = request.state.node

    id_successor = node.find_successor(id)
    if id_successor:
        return id_successor.serialize()

    raise HTTPException(
        status_code=404, detail=f"successor of '{id}' not found!")
