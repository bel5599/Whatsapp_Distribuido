from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode, DataBaseModel


router = APIRouter(prefix="/info", tags=["info"])


@router.get("/fingers_with_predecessor")
def fingers_predecessor_list(request: Request):
    node: EntityNode = request.state.node

    return [{"ip": ip, "port": port} for (ip, port) in node.fingers_predecessor_list()]


@router.get("/entity/{nickname}")
def nickname_entity_node(nickname: str, model: DataBaseModel, request: Request):
    node: EntityNode = request.state.node

    entity = node.nickname_entity_node(nickname, model.database_original)
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
