from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.repo.base import BaseRepo
from infrastructure.database.models.feature import Feature


class FeatureRepo(BaseRepo):
    async def create_feature_ticket(
        self, user_id: int, feature_message: str, software: str, username: Optional[str] = None
    ):
        insert_stmt = insert(Feature).values(
            user_id=user_id,
            feature_message=feature_message,
            software=software,
            username=username,
        )

        await self.session.execute(insert_stmt)

        await self.session.commit()

        return {"status": "success"}
