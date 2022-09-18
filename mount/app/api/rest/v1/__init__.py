from __future__ import annotations

from app.api.rest.v1 import (
    chats,
)
from fastapi import APIRouter

router = APIRouter()

router.include_router(chats.router, tags=["chats"])
