from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode, UserModel

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/entity{nickname}")
def nickname_entity_node(nickname, request:Request):
    node: EntityNode = request.state.node

    try:
        result = node.nickname_entity_node(nickname)
    except:
        raise HTTPException(
            status_code=500, detail="add user failed!")
    else:
        return result.serialize()


@router.put("/add")
def add_user(model: UserModel, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.add_user(model.nickname, model.password)
    except:
        raise HTTPException(
            status_code=500, detail="add user failed!")
    else:
        return {"success": result}


@router.delete("/delete/{nickname}")
def delete_user(nickname: str, request: Request):
    node: EntityNode = request.state.node

    try:
        result = node.delete_user(nickname)
    except:
        raise HTTPException(
            status_code=500, detail="delete user failed!")
    else:
        return {"success": result}
