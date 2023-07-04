from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/")
def search_chat_id(user_1, user_2, request: Request):
    node: EntityNode = request.state.node

    try:
        chat_id = node.search_chat_id(user_1, user_2)
    except:
        raise HTTPException(status_code=404, detail="chat id not found!")
    else:
        return {"chat_id": chat_id}


@router.put("/add")
def add_chat(user_1, user_2, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.add_chat(user_1, user_2)
    except:
        raise HTTPException(
            status_code=500, detail="add chat failed!")
    else:
        return {"success": result}


@router.delete("/delete/{user_1}/{user_2}")
def delete_chat(user_1, user_2, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_chat(user_1, user_2)
    except:
        raise HTTPException(
            status_code=500, detail="delete chat failed!")
    else:
        return {"success": result}

@router.get("/search/{user_1}/{user_2}")
def search_chat(user_1, user_2, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.search_chat(user_1, user_2)
    except:
        raise HTTPException(
            status_code=500, detail="search chat failed!")
    else:
        return [{"value": value} for (_,value) in result]