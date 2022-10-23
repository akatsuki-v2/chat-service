from __future__ import annotations

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models import Status
from app.models.chats import Chat
from app.models.chats import ChatInput
from app.models.chats import ChatUpdate
from app.usecases import chats
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


# https://osuakatsuki.atlassian.net/browse/V2-81
@router.post("/v1/chats", response_model=Success[Chat])
async def create_chat(args: ChatInput, ctx: RequestContext = Depends()):
    data = await chats.create(ctx, name=args.name, topic=args.topic,
                              read_privileges=args.read_privileges,
                              write_privileges=args.write_privileges,
                              auto_join=args.auto_join, instance=args.instance,
                              created_by=args.created_by)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create chat")

    resp = Chat.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-82
@router.get("/v1/chats/{chat_id}", response_model=Success[Chat])
async def get_chat(chat_id: int, ctx: RequestContext = Depends()):
    data = await chats.fetch_one(ctx, chat_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch chat")

    resp = Chat.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-83
@router.get("/v1/chats", response_model=Success[list[Chat]])
async def get_chats(name: str | None = None,
                    topic: str | None = None,
                    read_privileges: int | None = None,
                    write_privileges: int | None = None,
                    auto_join: bool | None = None,
                    status: Status | None = None,
                    created_by: int | None = None,
                    ctx: RequestContext = Depends()):
    data = await chats.fetch_all(ctx, name=name, topic=topic,
                                 read_privileges=read_privileges,
                                 write_privileges=write_privileges,
                                 auto_join=auto_join, status=status,
                                 created_by=created_by)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get chats")

    resp = [Chat.from_mapping(rec) for rec in data]
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-84
@router.patch("/v1/chats/{chat_id}", response_model=Success[Chat])
async def partial_update_chat(chat_id: int, args: ChatUpdate,
                              ctx: RequestContext = Depends()):
    data = await chats.partial_update(ctx, chat_id, **args.dict())
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update chat")

    resp = Chat.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-85
@router.delete("/v1/chats/{chat_id}", response_model=Success[Chat])
async def delete_chat(chat_id: int, ctx: RequestContext = Depends()):
    data = await chats.delete(ctx, chat_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete chat")

    resp = Chat.from_mapping(data)
    return responses.success(resp)
