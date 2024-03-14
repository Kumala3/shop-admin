from typing import Optional
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models.error import Error
from .base import BaseRepo


class ErrorRepo(BaseRepo):
    """Repository class for handling error tickets."""

    async def create_error_ticket(
        self,
        user_id: int,
        error_message: str,
        software: str,
        username: Optional[str] = None,
    ):
        """
        Create an error ticket.

        Args:
            user_id (int): The ID of the user reporting the error.
            error_message (str): The error message.
            software (str): The software where the error occurred.
            username (Optional[str], optional): The username of the user reporting the error. Defaults to None.

        Returns:
            dict: A dictionary indicating the status of the operation.
        """
        insert_stmt = insert(Error).values(
            user_id=user_id,
            error_message=error_message,
            software=software,
            username=username,
        )

        await self.session.execute(insert_stmt)

        await self.session.commit()

        return {"status": "success"}
