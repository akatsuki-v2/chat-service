from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    CHATS_CANNOT_CREATE = 'chats.cannot_create'
    CHATS_CANNOT_UPDATE = 'chats.cannot_update'
    CHATS_CANNOT_DELETE = 'chats.cannot_delete'
    CHATS_NOT_FOUND = 'chats.not_found'
