from fastapi import APIRouter, Request, HTTPException

# from ..base_node import BaseNodeModel
# from ..node import Node
# from ..remote_node import RemoteNode


router = APIRouter(prefix="/data", tags=["data"])