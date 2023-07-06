from fastapi import APIRouter, Request

from . import successor, predecessor, fingers
from .debug import router as debug_router
from ..node import Node


router = APIRouter(prefix="/chord", tags=["chord-protocol"])

router.include_router(successor.router)
router.include_router(predecessor.router)
router.include_router(fingers.router)


@router.get("/capacity")
def get_network_capacity(request: Request):
    node: Node = request.state.node

    capacity = node.network_capacity()
    return capacity
