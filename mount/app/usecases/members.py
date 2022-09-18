from typing import Any
from uuid import UUID

from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories.members import MembersRepo


async def create(ctx: Context,
                 chat_id: int,
                 session_id: UUID,
                 account_id: int,
                 username: str,
                 privileges: int,
                 ) -> dict[str, Any] | ServiceError:
    repo = MembersRepo(ctx)

    member = await repo.create(chat_id, session_id, account_id, username,
                               privileges)

    return member


async def fetch_one(ctx: Context, chat_id: int, session_id: UUID) -> dict[str, Any] | ServiceError:
    repo = MembersRepo(ctx)

    member = await repo.fetch_one(chat_id, session_id)
    if member is None:
        return ServiceError.MEMBERS_NOT_FOUND

    return member


async def fetch_all(ctx: Context, chat_id: int) -> list[dict[str, Any]]:
    repo = MembersRepo(ctx)

    members = await repo.fetch_all(chat_id)

    return members


async def partial_update(ctx: Context,
                         chat_id: int,
                         session_id: UUID,
                         username: str | None = None,
                         privileges: int | None = None,
                         ) -> dict[str, Any] | ServiceError:
    repo = MembersRepo(ctx)

    member = await repo.partial_update(chat_id, session_id,
                                       username=username,
                                       privileges=privileges)
    if member is None:
        return ServiceError.MEMBERS_NOT_FOUND

    return member


async def delete(ctx: Context, chat_id: int, session_id: UUID) -> dict[str, Any] | ServiceError:
    repo = MembersRepo(ctx)

    member = await repo.delete(chat_id, session_id)
    if member is None:
        return ServiceError.MEMBERS_NOT_FOUND

    return member
