from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode, ChatModel

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/")
def search_chat_id(model: ChatModel, request: Request):
    node: EntityNode = request.state.node

    try:
        chat_id = node.search_chat_id(model.user_id_1, model.user_id_2, model.database_original)
    except:
        raise HTTPException(status_code=404, detail="chat id not found!")
    else:
        return {"chat_id": chat_id}


@router.put("/add")
def add_chat(model: ChatModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.add_chat(model.user_id_1, model.user_id_2, model.database_original)
    except:
        raise HTTPException(
            status_code=500, detail="add chat failed!")
    else:
        return {"success": result}


@router.delete("/delete")
def delete_chat(model: ChatModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_chat(model.user_id_1, model.user_id_2, model.database_original)
    except:
        raise HTTPException(
            status_code=500, detail="delete chat failed!")
    else:
        return {"success": result}

@router.get("/search")
def search_chat(model: ChatModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_chat(model.user_id_1, model.user_id_2, model.database_original)
    except:
        raise HTTPException(
            status_code=500, detail="search chat failed!")
    else:
        return [{"value": value} for (_,value) in result]