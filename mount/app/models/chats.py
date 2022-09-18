from datetime import datetime

from app.models import BaseModel
from app.models import Status


class Chat(BaseModel):
    chat_id: int
    name: str
    topic: str
    read_privileges: int
    write_privileges: int
    auto_join: bool

    status: Status
    updated_at: datetime
    created_at: datetime
    created_by: int


class ChatInput(BaseModel):
    name: str
    topic: str
    read_privileges: int
    write_privileges: int
    auto_join: bool
    created_by: int


class ChatUpdate(BaseModel):
    name: str | None
    topic: str | None
    read_privileges: int | None
    write_privileges: int | None
    auto_join: bool | None

    status: Status | None
