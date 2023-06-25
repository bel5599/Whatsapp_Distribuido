from fastapi import APIRouter, Request

from ..base_node import BaseNode


router = APIRouter(prefix="/successor", tags=["successor"])


@router.get("/")
def get_successor(request: Request):
    node: BaseNode = request.state.node

    return node.successor().serialize()


@router.get("/{id}")
def find_successor(id: int, request: Request):
    node: BaseNode = request.state.node

    return node.find_successor(id).serialize()
