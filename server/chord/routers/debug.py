from fastapi import APIRouter, Request, HTTPException

from ..node import Node


router = APIRouter(prefix="/chord-debug", tags=["chord-protocol", "debug"])


@router.get("/me")
def get_node(request: Request):
    node: Node = request.state.node

    return node.serialize()


@router.get("/fingers")
def get_fingers(request: Request):
    node: Node = request.state.node

    return [finger.serialize() for finger in node.fingers]


@router.get("/fingers/{index}")
def get_finger(index: int, request: Request):
    node: Node = request.state.node

    try:
        finger = node.fingers[index]
        return finger.serialize()
    except:
        raise HTTPException(
            500, detail=f"index '{index}' must be lower than {node.network_capacity()}!")
