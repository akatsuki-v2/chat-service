from datetime import datetime
from uuid import UUID

from app.models import BaseModel


class Member(BaseModel):
    session_id: UUID
    account_id: int
    chat_id: int
    username: str
    privileges: int

    joined_at: datetime


class MemberInput(BaseModel):
    session_id: UUID
    account_id: int
    username: str
    privileges: int


class MemberUpdate(BaseModel):
    username: str | None
    privileges: int | None
