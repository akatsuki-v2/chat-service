from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    CHAT_CONFIGS_CANNOT_CREATE = 'chat_configs.cannot_create'
    CHAT_CONFIGS_CANNOT_UPDATE = 'chat_configs.cannot_update'
    CHAT_CONFIGS_CANNOT_DELETE = 'chat_configs.cannot_delete'
    CHAT_CONFIGS_NOT_FOUND = 'chat_configs.not_found'
