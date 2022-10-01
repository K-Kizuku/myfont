from fastapi import APIRouter
from .users import user_router
from .fonts import font_router
from .email import email_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(font_router, prefix="/fonts", tags=["fonts"])
router.include_router(email_router, prefix="/email", tags=["email"])