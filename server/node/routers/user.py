from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from ..entity_node import EntityNode


class UserModel(BaseModel):
    nickname: str
    password: str


router = APIRouter(prefix="/user", tags=["user"])


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
