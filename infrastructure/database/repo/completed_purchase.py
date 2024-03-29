from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, distinct

from .base import BaseRepo
from infrastructure.database.models.completed_purchase import CompletedPurchase
from infrastructure.database.models.purchase import Purchase

class CompletedPurchaseRepo(BaseRepo):
    """
    A class representing a repository for handling completed purchase database operations.

    Attributes:
        session (AsyncSession): The database session used by the repository.

    """

    async def create_completed_order(self, purchase: Purchase):
        """
        Create a new completed purchase in the database.

        Args:
            user_id (int): The ID of the user making the purchase.
            software (str): The name of the software being purchased.
            username (str): The username associated with the purchase.

        Returns:
            CompletedPurchase: The created completed purchase.

        """
        insert_stmt = insert(CompletedPurchase).values(
            user_id=purchase.user_id,
            software=purchase.software,
            username=purchase.username,
        )

        await self.session.execute(insert_stmt)

        await self.session.commit()

        return {"status": "success"}

    async def get_customers_ids(self):
        """
        Get a list of all customer IDs.

        Returns:
            list: A list of all customer IDs.

        """
        select_stmt = select(distinct(CompletedPurchase.user_id))

        result = await self.session.execute(select_stmt)

        return result.scalars().all()
