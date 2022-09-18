from __future__ import annotations

from app.api.rest.v1 import chats
from app.api.rest.v1 import members
from fastapi import APIRouter

router = APIRouter()

router.include_router(chats.router, tags=["chats"])
router.include_router(members.router, tags=["members"])
