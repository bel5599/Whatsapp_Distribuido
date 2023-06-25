from fastapi import APIRouter, Request, HTTPException

from ..base_node import BaseNode, BaseNodeModel


router = APIRouter(prefix="/fingers", tags=["fingers"])


@router.get("/capacity")
def get_network_capacity(request: Request):
    node: BaseNode = request.state.node

    capacity = node.network_capacity()
    if capacity is not None:
        return {"capacity": capacity}

    raise HTTPException(
        status_code=403, detail="getting network capacity failed!")


@router.get("/closest_preceding/{id}")
def get_closest_preceding_finger(id: int, request: Request):
    node: BaseNode = request.state.node

    closest = node.closest_preceding_finger(id)
    if closest:
        return closest.serialize()

    raise HTTPException(
        status_code=403, detail=f"closest preceding finger of {id} not found!")


@router.put("/update/{index}")
def update_fingers(index: int, model: BaseNodeModel, request: Request):
    node: BaseNode = request.state.node
    new_node = BaseNode.from_base_model(model)

    success = node.update_fingers(new_node, index)
    if success:
        return node.serialize()

    raise HTTPException(
        status_code=403, detail=f"updating fingers at {index} failed!")
