from fastapi import APIRouter, Request, HTTPException

from ..base_node import BaseNode


router = APIRouter(prefix="/successor", tags=["successor"])


@router.get("/")
def get_successor(request: Request):
    node: BaseNode = request.state.node

    successor = node.successor()
    if successor:
        return successor.serialize()

    raise HTTPException(status_code=403, detail="successor not found!")


@router.get("/{id}")
def find_successor(id: int, request: Request):
    node: BaseNode = request.state.node

    id_successor = node.find_successor(id)
    if id_successor:
        return id_successor.serialize()

    raise HTTPException(
        status_code=403, detail=f"successor of '{id}' not found!")
