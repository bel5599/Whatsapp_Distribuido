from fastapi import APIRouter, Request

from ..base_node import BaseNode, BaseNodeModel


router = APIRouter(prefix="/predecessor", tags=["predecessor"])


@router.get("/")
def get_predecessor(request: Request):
    node: BaseNode = request.state.node

    return node.predecessor().serialize()


@router.put("/")
def set_predecessor(model: BaseNodeModel, request: Request):
    node: BaseNode = request.state.node
    new_node = BaseNode.from_base_model(model)

    node.set_predecessor(new_node)

    return new_node.serialize()
