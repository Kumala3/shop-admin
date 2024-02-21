from typing import Optional
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models.error import Error
from infrastructure.database.models.users import User
from infrastructure.database.repo.base import BaseRepo


class ErrorRepo(BaseRepo):
    async def create_error_ticket(
        self,
        user_id: int,
        error_message: str,
        software: str,
        username: Optional[str] = None,
    ):
        insert_stmt = insert(Error).values(
            user_id=user_id,
            error_message=error_message,
            software=software,
            username=username,
        )

        await self.session.execute(insert_stmt)

        await self.session.commit()

        return {"status": "success"}
