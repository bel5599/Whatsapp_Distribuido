from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode, MessengerModel, SearchMessengerModel

router = APIRouter(prefix="/messenger", tags=["messenger"])


@router.get("/from")
def search_messenger_from(model: SearchMessengerModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_messenger_from(model.source, model.destiny, model.database_original)
    except:
        raise HTTPException(status_code=404, detail="messenges not found!")
    else:
        return [{"user_id_from":user_id_from, "value": value} for (user_id_from, value) in result]


@router.get("/to")
def search_messenger_to(model: SearchMessengerModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_messenger_to(model.source, model.destiny, model.database_original)
    except:
        raise HTTPException(status_code=404, detail="messenges not found!")
    else:
        return [{"user_id_from":user_id_from, "value": value} for (user_id_from, value) in result]


@router.put("/add")
def add_messenger(model: MessengerModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.add_messenger(model.source, model.destiny, model.value, model.database_original)
    except:
        raise HTTPException(
            status_code=500, detail="add messenger failed!")
    else:
        return {"success": result}


@router.delete("/delete/{id}")
def delete_messenger(id: int, database_original: bool, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_messenger(id, database_original)
    except:
        raise HTTPException(
            status_code=500, detail="delete messenger failed!")
    else:
        return {"success": result}
