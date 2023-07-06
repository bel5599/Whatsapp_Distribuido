from fastapi import APIRouter, Request, HTTPException

from ..base_node import BaseNodeModel
from ..node import Node
from ..remote_node import RemoteNode


router = APIRouter(prefix="/fingers")


@router.get("/closest_preceding/{id}")
def get_closest_preceding_finger(id: int, request: Request):
    node: Node = request.state.node

    try:
        closest = node.closest_preceding_finger(id)
    except:
        raise HTTPException(
            status_code=404, detail=f"closest preceding finger of {id} not found!")
    else:
        return closest.serialize()


@router.put("/update/{index}")
def update_fingers(index: int, model: BaseNodeModel, request: Request):
    node: Node = request.state.node

    try:
        new_node = RemoteNode.from_base_model(model)
        node.update_fingers(new_node, index)
    except:
        raise HTTPException(
            status_code=500, detail=f"updating fingers at {index} failed!")
    else:
        return node.serialize()
