from fastapi import APIRouter, Request, HTTPException

from ..node import Node


router = APIRouter(prefix="/fingers")


@router.get("/closest_preceding/{id}")
def get_closest_preceding_finger(id: int, request: Request):
    node: Node = request.state.node

    closest = node.closest_preceding_finger(id)
    if closest:
        return closest.serialize()

    raise HTTPException(
        status_code=404, detail=f"closest preceding finger of {id} not found!")
