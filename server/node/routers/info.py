from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode
from ..models import DataBaseModel, CopyDataBaseModel


router = APIRouter(prefix="/info", tags=["info"])


@router.get("/entity/{nickname}")
def nickname_entity_node(nickname: str, model: DataBaseModel, request: Request):
    node: EntityNode = request.state.node

    entity = node.nickname_entity_node(nickname, model.database_id)
    if entity:
        return entity.serialize()

    raise HTTPException(
        status_code=500, detail="node search failed!")


@router.get("/search_entity/{nickname}")
def search_entity_node(nickname: str, request: Request):
    node: EntityNode = request.state.node

    entity = node.search_entity_node(nickname)
    if entity:
        return entity.serialize()

    raise HTTPException(
        status_code=500, detail="node search failed!")


@router.get("/replicate")
def replicate(model: CopyDataBaseModel, request: Request):
    node: EntityNode = request.state.node

    try:
        node.replicate(model.source, model.database_id)
        return node.serialize()
    except:
        raise HTTPException(
            status_code=500, detail="replicate database failed!")


@router.get("/users")
def get_users(model: DataBaseModel, request: Request):
    node: EntityNode = request.state.node

    try:
        users = node.get_users(model.database_id)
    except:
        raise HTTPException(
            status_code=500, detail="get users failed!"
        )
    else:
        return {"users": users}
