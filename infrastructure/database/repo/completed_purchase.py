from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from .base import BaseRepo
from infrastructure.database.models.completed_purchase import CompletedPurchase


class CompletedPurchaseRepo(BaseRepo):
    """
    A class representing a repository for handling completed purchase database operations.

    Attributes:
        session (AsyncSession): The database session used by the repository.

    """

    async def create_completed_order(self, completed_purchase: CompletedPurchase):
        """
        Create a new completed purchase in the database.

        Args:
            user_id (int): The ID of the user making the purchase.
            software (str): The name of the software being purchased.
            payment_method (str): The payment method used for the purchase.
            username (str): The username associated with the purchase.

        Returns:
            CompletedPurchase: The created completed purchase.

        """
        insert_stmt = insert(CompletedPurchase).values(
            user_id=completed_purchase.user_id,
            software=completed_purchase.software,
            payment_method=completed_purchase.payment_method,
            username=completed_purchase.username,
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
        select_stmt = select(CompletedPurchase.user_id)

        result = await self.session.execute(select_stmt)

        return result.scalars().all()
