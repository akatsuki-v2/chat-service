from uuid import UUID

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.members import Member
from app.models.members import MemberInput
from app.usecases import members
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


# https://osuakatsuki.atlassian.net/browse/V2-86
@router.post("/v1/chats/{chat_id}/members", response_model=Success[Member])
async def join_chat(chat_id: int, args: MemberInput,
                    ctx: RequestContext = Depends()):
    data = await members.join_chat(ctx, chat_id, **args.dict())
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to add member")

    resp = Member.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-87
@router.delete("/v1/chats/{chat_id}/members/{session_id}",
               response_model=Success[Member])
async def leave_chat(chat_id: int, session_id: UUID,
                     ctx: RequestContext = Depends()):
    data = await members.leave_chat(ctx, chat_id, session_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to remove member")

    resp = Member.from_mapping(data)
    return responses.success(resp)


# https://osuakatsuki.atlassian.net/browse/V2-88
@router.get("/v1/chats/{chat_id}/members", response_model=Success[list[Member]])
async def get_members(chat_id: int, ctx: RequestContext = Depends()):
    data = await members.fetch_all(ctx, chat_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get members")

    resp = [Member.from_mapping(rec) for rec in data]
    return responses.success(resp)

# TODO: fetch_one? (models/repos/usecases are in place)
# TODO: update? (models/repos/usecases are in place)
