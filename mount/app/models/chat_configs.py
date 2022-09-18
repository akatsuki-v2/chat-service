from datetime import datetime

from app.models import BaseModel
from app.models import Status


class ChatConfig(BaseModel):
    name: str
    topic: str
    read_privileges: int
    write_privileges: int
    auto_join: bool

    status: Status
    updated_at: datetime
    created_at: datetime
    created_by: int


class ChatConfigInput(BaseModel):
    name: str
    topic: str
    read_privileges: int
    write_privileges: int
    auto_join: bool
    created_by: int


class ChatConfigUpdate(BaseModel):
    name: str | None
    topic: str | None
    read_privileges: int | None
    write_privileges: int | None
    auto_join: bool | None

    status: Status | None
