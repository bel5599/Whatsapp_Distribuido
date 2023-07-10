from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode, MessengerModel, SearchMessengerModel, DataBaseModel


router = APIRouter(prefix="/messenges", tags=["messenges"])


@router.get("/from")
def search_messenges_from(model: SearchMessengerModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_messenges_from(
            model.source, model.destiny, model.database_id)
    except:
        raise HTTPException(status_code=404, detail="messenges not found!")
    else:
        return [{"user_id_from": user_id_from, "value": value} for (user_id_from, value) in result]


@router.get("/to")
def search_messenges_to(model: SearchMessengerModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_messenges_to(
            model.source, model.destiny, model.database_id)
    except:
        raise HTTPException(status_code=404, detail="messenges not found!")
    else:
        return [{"user_id_from": user_id_from, "value": value} for (user_id_from, value) in result]

# ARREGLAR result


@router.get("/")
def get_messages(model: DataBaseModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.get_messages(model.database_id)
    except:
        raise HTTPException(status_code=404, detail="messenges not found!")
    else:
        return None


@router.put("/add")
def add_messenges(model: MessengerModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.add_messenges(
            model.source, model.destiny, model.value, model.database_id)
    except:
        raise HTTPException(
            status_code=500, detail="add messenger failed!")
    else:
        return {"success": result}


@router.delete("/delete/{id}")
def delete_messenges(id: int, model: DataBaseModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_messenges(id, model.database_id)
    except:
        raise HTTPException(
            status_code=500, detail="delete messenger failed!")
    else:
        return {"success": result}


@router.delete("/delete/to/{me}")
def delete_messenges_to(me: str, model: DataBaseModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_messenges_to(me, model.database_id)
    except:
        raise HTTPException(
            status_code=500, detail="delete messenger failed!")
    else:
        return {"success": result}


@router.delete("/delete/from/{me}")
def delete_messenges_from(me: str, model: DataBaseModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_messenges_from(me, model.database_id)
    except:
        raise HTTPException(
            status_code=500, detail="delete messenger failed!")
    else:
        return {"success": result}
