from __future__ import annotations

import traceback
from collections.abc import Mapping
from typing import Any

from app.common import logging
from app.common.context import Context
from app.common.errors import ServiceError
from app.models import Status
from app.repositories.chats import ChatsRepo


async def create(ctx: Context,
                 name: str,
                 topic: str,
                 read_privileges: int,
                 write_privileges: int,
                 auto_join: bool,
                 created_by: int,
                 ) -> Mapping[str, Any] | ServiceError:
    repo = ChatsRepo(ctx)

    transaction = await ctx.db.transaction()

    try:
        chat = await repo.create(name, topic, read_privileges,
                                 write_privileges, auto_join, created_by)
    except Exception as exc:
        await transaction.rollback()
        logging.error("Unable to create chat:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.CHATS_CANNOT_CREATE
    else:
        await transaction.commit()

    return chat


async def fetch_one(ctx: Context, chat_id: int) -> Mapping[str, Any] | ServiceError:
    repo = ChatsRepo(ctx)

    chat = await repo.fetch_one(chat_id)
    if chat is None:
        return ServiceError.CHATS_NOT_FOUND

    return chat


async def fetch_all(ctx: Context,
                    name: str | None = None,
                    topic: str | None = None,
                    read_privileges: int | None = None,
                    write_privileges: int | None = None,
                    auto_join: bool | None = None,
                    status: Status | None = None,
                    created_by: int | None = None) -> list[Mapping[str, Any]]:
    repo = ChatsRepo(ctx)

    return await repo.fetch_all(name=name,
                                topic=topic,
                                read_privileges=read_privileges,
                                write_privileges=write_privileges,
                                auto_join=auto_join,
                                status=status,
                                created_by=created_by)


async def partial_update(ctx: Context,
                         chat_id: int,
                         name: str | None = None,
                         topic: str | None = None,
                         read_privileges: int | None = None,
                         write_privileges: int | None = None,
                         auto_join: bool | None = None,
                         status: Status | None = None,
                         ) -> Mapping[str, Any] | ServiceError:
    repo = ChatsRepo(ctx)

    transaction = await ctx.db.transaction()

    try:
        chat = await repo.partial_update(chat_id, name, topic,
                                         read_privileges, write_privileges,
                                         auto_join, status)
        if chat is None:
            await transaction.rollback()
            return ServiceError.CHATS_NOT_FOUND

    except Exception as exc:
        await transaction.rollback()
        logging.error("Unable to update chat:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.CHATS_CANNOT_UPDATE
    else:
        await transaction.commit()

    return chat


async def delete(ctx: Context, chat_id: int) -> Mapping[str, Any] | ServiceError:
    repo = ChatsRepo(ctx)

    transaction = await ctx.db.transaction()

    try:
        chat = await repo.delete(chat_id)
        if chat is None:
            await transaction.rollback()
            return ServiceError.CHATS_NOT_FOUND

    except Exception as exc:
        await transaction.rollback()
        logging.error("Unable to delete chat:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.CHATS_CANNOT_DELETE
    else:
        await transaction.commit()

    return chat
