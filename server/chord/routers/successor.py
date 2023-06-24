from fastapi import APIRouter, Request

from ..base_node import BaseNode


router = APIRouter(prefix="/successor", tags=["successor"])


@router.get("/")
async def get_successor(request: Request):
    node: BaseNode = request.state.node

    result_node = await node.successor()
    return result_node.serialize()


@router.get("/{id}")
async def find_successor(id: int, request: Request):
    node: BaseNode = request.state.node

    result_node = await node.find_successor(id)
    return result_node.serialize()
