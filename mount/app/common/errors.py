from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    CHATS_CANNOT_CREATE = 'chats.cannot_create'
    CHATS_CANNOT_UPDATE = 'chats.cannot_update'
    CHATS_CANNOT_DELETE = 'chats.cannot_delete'
    CHATS_NOT_FOUND = 'chats.not_found'

    MEMBERS_CANNOT_CREATE = 'members.cannot_create'
    MEMBERS_CANNOT_UPDATE = 'members.cannot_update'
    MEMBERS_CANNOT_DELETE = 'members.cannot_delete'
    MEMBERS_NOT_FOUND = 'members.not_found'
