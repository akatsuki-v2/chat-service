from datetime import datetime
from typing import Any
from typing import Literal
from uuid import UUID

from app.common import json as jsonu
from app.common.context import Context


def create_member_key(chat_id: int, session_id: Literal['*'] | UUID) -> str:
    return f"chats:{chat_id}:members:{session_id}"


class MembersRepo:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self, chat_id: int, session_id: UUID, account_id: int,
                     username: str, privileges: int) -> dict[str, Any]:
        session = {
            "chat_id": chat_id,
            "session_id": session_id,
            "account_id": account_id,
            "username": username,
            "privileges": privileges,
            "joined_at": datetime.now().isoformat(),
        }
        await self.ctx.redis.set(create_member_key(chat_id, session_id),
                                 jsonu.dumps(session))
        return session

    async def fetch_one(self, chat_id: int, session_id: UUID) -> dict[str, Any] | None:
        session = await self.ctx.redis.get(create_member_key(chat_id, session_id))
        if session is None:
            return None
        return jsonu.loads(session)

    async def fetch_all(self, chat_id: int) -> list[dict[str, Any]]:
        keys = await self.ctx.redis.keys(f"chats:{chat_id}:members:*")
        if not keys:
            return []

        sessions = await self.ctx.redis.mget(*keys)
        return [jsonu.loads(session) for session in sessions]

    async def partial_update(self, chat_id: int, session_id: UUID, **kwargs: Any) -> dict[str, Any] | None:
        session = await self.fetch_one(chat_id, session_id)
        if session is None:
            return None

        if not kwargs:
            return session

        session = dict(session)
        session.update(kwargs)

        await self.ctx.redis.set(create_member_key(chat_id, session_id), jsonu.dumps(session))
        return session

    async def delete(self, chat_id: int, session_id: UUID) -> dict[str, Any] | None:
        session = await self.fetch_one(chat_id, session_id)
        if session is None:
            return None

        await self.ctx.redis.delete(create_member_key(chat_id, session_id))

        return session
