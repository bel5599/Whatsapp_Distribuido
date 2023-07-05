from fastapi import APIRouter

from . import successor, predecessor, fingers
from .debug import router as debug_router


router = APIRouter(prefix="/chord", tags=["chord-protocol"])

router.include_router(successor.router)
router.include_router(predecessor.router)
router.include_router(fingers.router)
