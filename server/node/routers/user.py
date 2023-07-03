from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode, UserModel

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/pasword/{nickname}")
def get_pasword(nickname: str, request: Request):
    node: EntityNode = request.state.node

    try:
        pasw = node.get_pasword(nickname)
    except:
        raise HTTPException(
            status_code=500, detail="get pasword failed!")
    else:
        return {"pasword": pasw}

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
    

