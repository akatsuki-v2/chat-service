from __future__ import annotations

from app.api.rest.v1 import (
    chat_configs,
)
from fastapi import APIRouter

router = APIRouter()

router.include_router(chat_configs.router, tags=["chat-configs"])
