from fastapi import APIRouter, Request, HTTPException

from . import info, messages, user


router = APIRouter(prefix="/")

router.include_router(info.router)
router.include_router(messages.router)
router.include_router(user.router)


