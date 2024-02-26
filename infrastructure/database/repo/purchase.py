from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from infrastructure.database.models.purchase import Purchase
from .base import BaseRepo


class PurchaseRepo(BaseRepo):
    """Repository class for handling purchases."""

    async def create_purchase(
        self,
        user_id: int,
        software: str,
        payment_method: str,
        username: str,
    ):
        """
        Create a new purchase.

        Args:
            user_id (int): The ID of the user making the purchase.
            software (str): The name of the software being purchased.
            payment_method (str): The payment method used for the purchase.
            username (str): The username associated with the purchase.

        Returns:
            dict: A dictionary containing the status of the operation.
        """
        insert_stmt = insert(Purchase).values(
            user_id=user_id,
            software=software,
            payment_method=payment_method,
            username=username,
        )

        await self.session.execute(insert_stmt)

        await self.session.commit()

        return {"status": "success"}

    async def get_customers_ids(self):
        """
        Get a list of all customers who have made a purchase.

        Returns:
            list: A list containing customers ids.
        """
        select_stmt = select(Purchase.user_id)

        result = await self.session.execute(select_stmt)

        return result.scalars().all()
        
