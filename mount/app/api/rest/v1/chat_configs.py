from __future__ import annotations

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models import Status
from app.models.chat_configs import ChatConfig
from app.models.chat_configs import ChatConfigInput
from app.models.chat_configs import ChatConfigUpdate
from app.usecases import chat_configs
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


# https://osuakatsuki.atlassian.net/browse/V2-81
@router.post("/v1/chat-configs", response_model=Success[ChatConfig])
async def create_chat_config(args: ChatConfigInput, ctx: RequestContext = Depends()):
    data = await chat_configs.create(ctx, **args.dict())
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create chat config")

    resp = ChatConfig.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-82
@router.get("/v1/chat-configs/{config_id}", response_model=Success[ChatConfig])
async def get_chat_config(config_id: int, ctx: RequestContext = Depends()):
    data = await chat_configs.fetch_one(ctx, config_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch chat config")

    resp = ChatConfig.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-83
@router.get("/v1/chat-configs", response_model=Success[list[ChatConfig]])
async def get_chat_configs(status: Status | None = Status.ACTIVE,
                           created_by: int | None = None,
                           ctx: RequestContext = Depends()):
    data = await chat_configs.fetch_all(ctx, status=status,
                                        created_by=created_by)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get chat configs")

    resp = [ChatConfig.from_mapping(acc) for acc in data]
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-84
@router.patch("/v1/chat-configs/{config_id}", response_model=Success[ChatConfig])
async def partial_update_chat_config(config_id: int, args: ChatConfigUpdate,
                                     ctx: RequestContext = Depends()):
    data = await chat_configs.partial_update(ctx, config_id, **args.dict())
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update chat config")

    resp = ChatConfig.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-85
@router.delete("/v1/chat-configs/{config_id}", response_model=Success[ChatConfig])
async def delete_chat_config(config_id: int, ctx: RequestContext = Depends()):
    data = await chat_configs.delete(ctx, config_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete chat config")

    resp = ChatConfig.from_mapping(data)
    return responses.success(resp)
