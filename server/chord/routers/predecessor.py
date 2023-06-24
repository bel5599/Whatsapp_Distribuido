from fastapi import APIRouter, Request

from ..base_node import BaseNode, BaseNodeModel


router = APIRouter(prefix="/predecessor", tags=["predecessor"])


@router.get("/")
async def get_predecessor(request: Request):
    node: BaseNode = request.state.node

    result_node = await node.predecessor()
    return result_node.serialize()


@router.put("/")
async def set_predecessor(model: BaseNodeModel, request: Request):
    node: BaseNode = request.state.node
    new_node = BaseNode.from_base_model(model)

    await node.set_predecessor(new_node)

    return new_node.serialize()
