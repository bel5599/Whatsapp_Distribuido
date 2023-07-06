from fastapi import APIRouter, Request, HTTPException

from . import successor, predecessor, fingers
from .debug import router as debug_router
from ..base_node import BaseNodeModel
from ..node import Node
from ..remote_node import RemoteNode


router = APIRouter(prefix="/chord", tags=["chord-protocol"])

router.include_router(successor.router)
router.include_router(predecessor.router)
router.include_router(fingers.router)


@router.get("/capacity")
def get_network_capacity(request: Request):
    node: Node = request.state.node

    capacity = node.network_capacity()
    return capacity


@router.get("/heart")
def beat(request: Request):
    node: Node = request.state.node

    return node.heart()


@router.put("/notify")
def notify(model: BaseNodeModel, request: Request):
    node: Node = request.state.node

    try:
        other = RemoteNode.from_base_model(model)
        node.notify(other)
    except:
        raise HTTPException(
            status_code=500, detail="setting predecessor failed!")
    else:
        return node.serialize()
