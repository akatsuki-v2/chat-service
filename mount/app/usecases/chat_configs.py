from __future__ import annotations

import traceback
from collections.abc import Mapping
from typing import Any

from app.common import logging
from app.common.context import Context
from app.common.errors import ServiceError
from app.models import Status
from app.repositories.chat_configs import ChatConfigsRepo


async def create(ctx: Context,
                 name: str,
                 topic: str,
                 read_privileges: int,
                 write_privileges: int,
                 auto_join: bool,
                 created_by: int,
                 ) -> Mapping[str, Any] | ServiceError:
    repo = ChatConfigsRepo(ctx)

    transaction = await ctx.db.transaction()

    try:
        chat_config = await repo.create(name, topic, read_privileges,
                                        write_privileges, auto_join, created_by)
    except Exception as exc:
        await transaction.rollback()
        logging.error("Unable to create chat config:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.CHAT_CONFIGS_CANNOT_CREATE
    else:
        await transaction.commit()

    return chat_config


async def fetch_one(ctx: Context, config_id: int) -> Mapping[str, Any] | ServiceError:
    repo = ChatConfigsRepo(ctx)

    chat_config = await repo.fetch_one(config_id)
    if chat_config is None:
        return ServiceError.CHAT_CONFIGS_NOT_FOUND

    return chat_config


async def fetch_all(ctx: Context,
                    name: str | None = None,
                    topic: str | None = None,
                    read_privileges: int | None = None,
                    write_privileges: int | None = None,
                    auto_join: bool | None = None,
                    status: Status | None = None,
                    created_by: int | None = None) -> list[Mapping[str, Any]]:
    repo = ChatConfigsRepo(ctx)

    return await repo.fetch_all(name=name,
                                topic=topic,
                                read_privileges=read_privileges,
                                write_privileges=write_privileges,
                                auto_join=auto_join,
                                status=status,
                                created_by=created_by)


async def partial_update(ctx: Context,
                         config_id: int,
                         name: str | None = None,
                         topic: str | None = None,
                         read_privileges: int | None = None,
                         write_privileges: int | None = None,
                         auto_join: bool | None = None,
                         status: Status | None = None,
                         ) -> Mapping[str, Any] | ServiceError:
    repo = ChatConfigsRepo(ctx)

    transaction = await ctx.db.transaction()

    try:
        chat_config = await repo.partial_update(config_id, name, topic,
                                                read_privileges, write_privileges,
                                                auto_join, status)
        if chat_config is None:
            await transaction.rollback()
            return ServiceError.CHAT_CONFIGS_NOT_FOUND

    except Exception as exc:
        await transaction.rollback()
        logging.error("Unable to update chat config:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.CHAT_CONFIGS_CANNOT_UPDATE
    else:
        await transaction.commit()

    return chat_config


async def delete(ctx: Context, config_id: int) -> Mapping[str, Any] | ServiceError:
    repo = ChatConfigsRepo(ctx)

    transaction = await ctx.db.transaction()

    try:
        chat_config = await repo.delete(config_id)
        if chat_config is None:
            await transaction.rollback()
            return ServiceError.CHAT_CONFIGS_NOT_FOUND

    except Exception as exc:
        await transaction.rollback()
        logging.error("Unable to delete chat config:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.CHAT_CONFIGS_CANNOT_DELETE
    else:
        await transaction.commit()

    return chat_config
