from fastapi import APIRouter

from . import info, messages, user


router = APIRouter()

router.include_router(info.router)
router.include_router(messages.router)
router.include_router(user.router)
