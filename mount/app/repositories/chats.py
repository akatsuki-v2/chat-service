from typing import Any
from typing import Mapping

from app.common.context import Context
from app.models import Status


class ChatsRepo:
    READ_PARAMS = """\
        chat_id, name, topic, read_privileges, write_privileges, auto_join,
        status, updated_at, created_at, created_by
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self,
                     name: str,
                     topic: str,
                     read_privileges: int,
                     write_privileges: int,
                     auto_join: bool,
                     created_by: int,
                     status: Status = Status.ACTIVE,
                     ) -> Mapping[str, Any]:
        query = f"""\
            INSERT INTO chats (name, topic, read_privileges,
                                      write_privileges, auto_join, status,
                                      created_by)
                 VALUES (:name, :topic, :read_privileges, :write_privileges,
                         :auto_join, :status, :created_by)
        """
        params = {
            "name": name,
            "topic": topic,
            "read_privileges": read_privileges,
            "write_privileges": write_privileges,
            "auto_join": auto_join,
            "status": status,
            "created_by": created_by,
        }
        row_id = await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM chats
             WHERE chat_id = :chat_id
        """
        params = {"chat_id": row_id}
        chat = await self.ctx.db.fetch_one(query, params)
        assert chat is not None
        return chat


    async def fetch_one(self, chat_id: int | None = None,
                        name: str | None = None,
                        topic: str | None = None,
                        read_privileges: int | None = None,
                        write_privileges: int | None = None,
                        auto_join: bool | None = None,
                        status: Status | None = Status.ACTIVE,
                        created_by: int | None = None) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM chats
             WHERE chat_id = COALESCE(:chat_id, chat_id)
               AND name = COALESCE(:name, name)
               AND topic = COALESCE(:topic, topic)
               AND read_privileges = COALESCE(:read_privileges, read_privileges)
               AND write_privileges = COALESCE(:write_privileges, write_privileges)
               AND auto_join = COALESCE(:auto_join, auto_join)
               AND status = COALESCE(:status, status)
               AND created_by = COALESCE(:created_by, created_by)
        """
        params = {
            "chat_id": chat_id,
            "name": name,
            "topic": topic,
            "read_privileges": read_privileges,
            "write_privileges": write_privileges,
            "auto_join": auto_join,
            "status": status,
            "created_by": created_by,
        }
        chat = await self.ctx.db.fetch_one(query, params)
        return chat

    async def fetch_all(self, name: str | None = None,
                        topic: str | None = None,
                        read_privileges: int | None = None,
                        write_privileges: int | None = None,
                        auto_join: bool | None = None,
                        status: Status | None = Status.ACTIVE,
                        created_by: int | None = None) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM chats
             WHERE name = COALESCE(:name, name)
               AND topic = COALESCE(:topic, topic)
               AND read_privileges = COALESCE(:read_privileges, read_privileges)
               AND write_privileges = COALESCE(:write_privileges, write_privileges)
               AND auto_join = COALESCE(:auto_join, auto_join)
               AND status = COALESCE(:status, status)
               AND created_by = COALESCE(:created_by, created_by)
        """
        params = {
            "name": name,
            "topic": topic,
            "read_privileges": read_privileges,
            "write_privileges": write_privileges,
            "auto_join": auto_join,
            "status": status,
            "created_by": created_by,
        }
        chats = await self.ctx.db.fetch_all(query, params)
        return chats

    async def partial_update(self, chat_id: int,
                             name: str | None = None,
                             topic: str | None = None,
                             read_privileges: int | None = None,
                             write_privileges: int | None = None,
                             auto_join: bool | None = None,
                             status: Status | None = None) -> Mapping[str, Any] | None:
        query = f"""\
            UPDATE chats
               SET name = COALESCE(:name, name),
                   topic = COALESCE(:topic, topic),
                   read_privileges = COALESCE(:read_privileges, read_privileges),
                   write_privileges = COALESCE(:write_privileges, write_privileges),
                   auto_join = COALESCE(:auto_join, auto_join),
                   status = COALESCE(:status, status),
                   updated_at = CURRENT_TIMESTAMP
             WHERE chat_id = :chat_id
        """
        params = {
            "chat_id": chat_id,
            "name": name,
            "topic": topic,
            "read_privileges": read_privileges,
            "write_privileges": write_privileges,
            "auto_join": auto_join,
            "status": status,
        }
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM chats
             WHERE chat_id = :chat_id
        """
        params = {"chat_id": chat_id}
        chat = await self.ctx.db.fetch_one(query, params)
        assert chat is not None
        return chat

    async def delete(self, chat_id: int) -> Mapping[str, Any] | None:
        query = f"""\
            UPDATE chats
               SET status = :deleted_status,
                   updated_at = CURRENT_TIMESTAMP
             WHERE chat_id = :chat_id
               AND status != :deleted_status
        """
        params = {
            "chat_id": chat_id,
            "deleted_status": Status.DELETED,
        }
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM chats
             WHERE chat_id = :chat_id
        """
        params = {"chat_id": chat_id}
        chat = await self.ctx.db.fetch_one(query, params)
        assert chat is not None
        return chat
