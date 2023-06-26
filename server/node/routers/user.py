from fastapi import APIRouter, Request, HTTPException

# from ..base_node import BaseNodeModel
from ..entity_node import EntityNode
from pydantic import BaseModel
# from ..remote_node import RemoteNode

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
        return {str(result): result}
    
@router.delete("/delete/{nickname}")
def delete_user(nickname: str, request: Request):
    node:EntityNode = request.state.node

    try:
        result = node.delete_user(nickname)
    except:
        raise HTTPException(
            status_code=500, detail="delete user failed!")
    else:
        return {str(result): result}
   