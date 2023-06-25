from fastapi import APIRouter, Request

from ..base_node import BaseNode, BaseNodeModel


router = APIRouter(prefix="/fingers", tags=["fingers"])


@router.get("/capacity")
def get_network_capacity(request: Request):
    node: BaseNode = request.state.node

    return {"capacity": node.network_capacity()}


@router.get("/closest_preceding/{id}")
def get_closest_preceding_finger(id: int, request: Request):
    node: BaseNode = request.state.node

    return node.closest_preceding_finger(id).serialize()


@router.put("/update/{index}")
def update_fingers(index: int, model: BaseNodeModel, request: Request):
    node: BaseNode = request.state.node
    new_node = BaseNode.from_base_model(model)

    node.update_fingers(new_node, index)

    return new_node.serialize()
