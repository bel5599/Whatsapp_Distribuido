from fastapi import APIRouter, Request, HTTPException

from ..entity_node import EntityNode


router = APIRouter(prefix="/info", tags=["info"])

@router.get("/fingers_with_predecessor")
def fingers_predecessor_list(request: Request):
    node : EntityNode = request.state.node

    return [{"ip": ip, "port": port} for (ip, port) in node.fingers_predecessor_list()]

@router.get("/entity/{nickname}")
def nickname_entity_node(nickname, request:Request):
    node: EntityNode = request.state.node

    try:
        result = node.nickname_entity_node(nickname)
    except:
        raise HTTPException(
            status_code=500, detail="node search failed!")
    else:
        if result is None:
            return {}
        return {"ip": result.ip, "port": result.port}
