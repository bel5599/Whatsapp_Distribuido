from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode
from ..models import MessengerModel, SearchMessengerModel, DataBaseModel


router = APIRouter(prefix="/messages", tags=["messages"])


# @router.get("/from")
# def search_messages_from(model: SearchMessengerModel, request: Request):
#     node: EntityNode = request.state.node

#     try:
#         result = node.search_messages_from(
#             model.source, model.destiny, model.database_id)
#     except:
#         raise HTTPException(status_code=404, detail="messages not found!")
#     else:
#         return [{"user_id_from": user_id_from, "value": value} for (user_id_from, value) in result]


@router.get("/to")
def search_messages_to(model: SearchMessengerModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_messages_to(
            model.source, model.destiny, model.database_id)
    except:
        raise HTTPException(status_code=404, detail="messages not found!")
    else:
        return [{"user_id_from": user_id_from, "value": value} for (user_id_from, value) in result]

# ARREGLAR result


# @router.get("/")
# def get_messages(model: DataBaseModel, request: Request):
#     node: EntityNode = request.state.node

#     try:
#         result = node.get_messages(model.database_id)
#     except:
#         raise HTTPException(status_code=404, detail="messages not found!")
#     else:
#         return None


@router.put("/add")
def add_messages(model: MessengerModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.add_messages(
            model.source, model.destiny, model.value, model.database_id)
    except:
        raise HTTPException(
            status_code=500, detail="add messages failed!")
    else:
        return {"success": result}


# @router.delete("/delete/{id}")
# def delete_messages(id: int, model: DataBaseModel, request: Request):
#     node: EntityNode = request.state.node

#     try:
#         result = node.delete_messages(id, model.database_id)
#     except:
#         raise HTTPException(
#             status_code=500, detail="delete messages failed!")
#     else:
#         return {"success": result}


@router.delete("/delete/to/{me}")
def delete_messages_to(me: str, model: DataBaseModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_messages_to(me, model.database_id)
    except:
        raise HTTPException(
            status_code=500, detail="delete messages failed!")
    else:
        return {"success": result}


# @router.delete("/delete/from/{me}")
# def delete_messages_from(me: str, model: DataBaseModel, request: Request):
#     node: EntityNode = request.state.node

#     try:
#         result = node.delete_messages_from(me, model.database_id)
#     except:
#         raise HTTPException(
#             status_code=500, detail="delete messages failed!")
#     else:
#         return {"success": result}
