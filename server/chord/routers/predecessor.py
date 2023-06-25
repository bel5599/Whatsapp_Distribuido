from fastapi import APIRouter, Request, HTTPException

from ..base_node import BaseNode, BaseNodeModel


router = APIRouter(prefix="/predecessor", tags=["predecessor"])


@router.get("/")
def get_predecessor(request: Request):
    node: BaseNode = request.state.node

    predecessor = node.predecessor()
    if predecessor:
        return predecessor.serialize()

    raise HTTPException(status_code=403, detail="predecessor not found!")


@router.put("/")
def set_predecessor(model: BaseNodeModel, request: Request):
    node: BaseNode = request.state.node
    new_node = BaseNode.from_base_model(model)

    success = node.set_predecessor(new_node)
    if success:
        return node.serialize()

    raise HTTPException(status_code=403, detail="setting predecessor failed!")
