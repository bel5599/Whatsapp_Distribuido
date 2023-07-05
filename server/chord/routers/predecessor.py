from fastapi import APIRouter, Request, HTTPException

from ..base_node import BaseNodeModel
from ..node import Node
from ..remote_node import RemoteNode


router = APIRouter(prefix="/predecessor")


@router.get("/")
def get_predecessor(request: Request):
    node: Node = request.state.node

    try:
        predecessor = node.predecessor()
    except:
        raise HTTPException(status_code=404, detail="predecessor not found!")
    else:
        return predecessor.serialize()


@router.put("/")
def set_predecessor(model: BaseNodeModel, request: Request):
    node: Node = request.state.node

    try:
        new_node = RemoteNode.from_base_model(model)
        node.set_predecessor(new_node)
    except:
        raise HTTPException(
            status_code=500, detail="setting predecessor failed!")
    else:
        return node.serialize()
