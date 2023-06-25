from fastapi import APIRouter, Request, HTTPException

from ..node import Node


router = APIRouter(prefix="/successor", tags=["successor"])


@router.get("/")
def get_successor(request: Request):
    node: Node = request.state.node

    try:
        successor = node.successor()
    except:
        raise HTTPException(status_code=404, detail="successor not found!")
    else:
        return successor.serialize()


@router.get("/{id}")
def find_successor(id: int, request: Request):
    node: Node = request.state.node

    try:
        id_successor = node.find_successor(id)
    except:
        raise HTTPException(
            status_code=404, detail=f"successor of '{id}' not found!")
    else:
        return id_successor.serialize()
