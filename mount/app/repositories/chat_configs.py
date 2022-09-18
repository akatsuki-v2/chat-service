from typing import Any
from typing import Mapping

from app.common.context import Context
from app.models import Status


class ChatConfigsRepo:
    READ_PARAMS = """\
        config_id, name, topic, read_privileges, write_privileges, auto_join,
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
            INSERT INTO chat_configs (name, topic, read_privileges,
                                      write_privileges, auto_join, status,
                                      created_by)
                 VALUES (:name, :topic, :read_privileges, :write_privileges,
                         :auto_join, :status, :created_by)
              RETURNING {self.READ_PARAMS}
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
        chat_config = await self.ctx.db.fetch_one(query, params)
        assert chat_config is not None
        return chat_config

    async def fetch_one(self, config_id: int | None = None,
                        name: str | None = None,
                        topic: str | None = None,
                        read_privileges: int | None = None,
                        write_privileges: int | None = None,
                        auto_join: bool | None = None,
                        status: Status | None = Status.ACTIVE,
                        created_by: int | None = None) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM chat_configs
             WHERE config_id = COALESCE(:config_id, config_id)
               AND name = COALESCE(:name, name)
               AND topic = COALESCE(:topic, topic)
               AND read_privileges = COALESCE(:read_privileges, read_privileges)
               AND write_privileges = COALESCE(:write_privileges, write_privileges)
               AND auto_join = COALESCE(:auto_join, auto_join)
               AND status = COALESCE(:status, status)
               AND created_by = COALESCE(:created_by, created_by)
            """
        params = {
            "config_id": config_id,
            "name": name,
            "topic": topic,
            "read_privileges": read_privileges,
            "write_privileges": write_privileges,
            "auto_join": auto_join,
            "status": status,
            "created_by": created_by,
        }
        chat_config = await self.ctx.db.fetch_one(query, params)
        return chat_config

    async def fetch_all(self, name: str | None = None,
                        topic: str | None = None,
                        read_privileges: int | None = None,
                        write_privileges: int | None = None,
                        auto_join: bool | None = None,
                        status: Status | None = Status.ACTIVE,
                        created_by: int | None = None) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM chat_configs
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
        chat_configs = await self.ctx.db.fetch_all(query, params)
        return chat_configs

    async def partial_update(self, config_id: int,
                             name: str | None = None,
                             topic: str | None = None,
                             read_privileges: int | None = None,
                             write_privileges: int | None = None,
                             auto_join: bool | None = None,
                             status: Status | None = None) -> Mapping[str, Any] | None:
        query = f"""\
            UPDATE chat_configs
               SET name = COALESCE(:name, name),
                   topic = COALESCE(:topic, topic),
                   read_privileges = COALESCE(:read_privileges, read_privileges),
                   write_privileges = COALESCE(:write_privileges, write_privileges),
                   auto_join = COALESCE(:auto_join, auto_join),
                   status = COALESCE(:status, status),
                   updated_at = CURRENT_TIMESTAMP
             WHERE config_id = :config_id
         RETURNING {self.READ_PARAMS}
                """
        params = {
            "config_id": config_id,
            "name": name,
            "topic": topic,
            "read_privileges": read_privileges,
            "write_privileges": write_privileges,
            "auto_join": auto_join,
            "status": status,
        }
        chat_config = await self.ctx.db.fetch_one(query, params)
        return chat_config

    async def delete(self, config_id: int) -> Mapping[str, Any] | None:
        query = f"""\
            UPDATE chat_configs
               SET status = :deleted_status,
                   updated_at = CURRENT_TIMESTAMP
             WHERE config_id = :config_id
               AND status != :deleted_status
         RETURNING {self.READ_PARAMS}
        """
        params = {
            "config_id": config_id,
            "deleted_status": Status.DELETED,
        }
        chat_config = await self.ctx.db.fetch_one(query, params)
        return chat_config
