from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.repo.base import BaseRepo
from infrastructure.database.models.feature import Feature


class FeatureRepo(BaseRepo):
    """Repository for managing feature tickets."""

    async def create_feature_ticket(
        self, user_id: int, feature_message: str, software: str, username: Optional[str] = None
    ):
        """
        Create a new feature ticket.

        Args:
            user_id (int): The ID of the user creating the ticket.
            feature_message (str): The message describing the feature.
            software (str): The software related to the feature.
            username (Optional[str]): The username of the user creating the ticket (default: None).

        Returns:
            dict: A dictionary with the status of the ticket creation.

        """
        insert_stmt = insert(Feature).values(
            user_id=user_id,
            feature_message=feature_message,
            software=software,
            username=username,
        )

        await self.session.execute(insert_stmt)

        await self.session.commit()

        return {"status": "success"}
