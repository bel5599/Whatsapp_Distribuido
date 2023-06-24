from fastapi import APIRouter, Request


from ..base_node import BaseNode, BaseNodeModel


router = APIRouter(prefix="/fingers", tags=["fingers"])


@router.get("/closest_preceding/{id}")
async def get_closest_preceding_finger(id: int, request: Request):
    node: BaseNode = request.state.node

    result_node = await node.closest_preceding_finger(id)
    return result_node.serialize()


@router.put("/update/{index}")
async def update_fingers(index: int, model: BaseNodeModel, request: Request):
    node: BaseNode = request.state.node
    new_node = BaseNode.from_base_model(model)

    await node.update_fingers(new_node, index)

    return new_node.serialize()
