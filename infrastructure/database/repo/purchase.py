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
            username=username,
        )

        await self.session.execute(insert_stmt)

        await self.session.commit()

        return {"status": "success", "purchase_id": insert_stmt.returning(Purchase.purchase_id)}

    async def get_purchase_by_id(self, purchase_id):
        """
        Get a purchase by ID.

        Args:
            purchase_id (int): The ID of the purchase to retrieve.

        Returns:
            Purchase: The purchase with the given ID.
        """
        select_stmt = select(Purchase).where(Purchase.purchase_id == purchase_id)

        result = await self.session.execute(select_stmt)

        return result.scalar()

    async def get_customers_ids(self):
        """
        Get a list of all customers who have made a purchase.

        Returns:
            list: A list containing customers ids.
        """
        select_stmt = select(Purchase.user_id)

        result = await self.session.execute(select_stmt)

        return result.scalars().all()

    async def delete_purchase_by_id(self, purchase_id: int):
        """
        Delete a purchase by user ID.

        Args:
            user_id (int): The ID of the user whose purchase should be deleted.

        Returns:
            dict: A dictionary containing the status of the operation.
        """

        delete_stmt = Purchase.delete().where(Purchase.purchase_id == purchase_id)

        await self.session.execute(delete_stmt)

        await self.session.commit()

        return {"status": "purchase was successfully deleted"}
