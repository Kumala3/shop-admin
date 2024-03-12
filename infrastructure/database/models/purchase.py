from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, BigInteger

from infrastructure.database.models.base import Base, TableNameMixin, TimestampMixin

class Purchase(Base, TableNameMixin, TimestampMixin):
    """
    Represents a purchase made by a user.

    Attributes:
        purchase_id (int): The unique identifier for the purchase.
        user_id (int): The user ID associated with the purchase.
        product_id (int): The product ID associated with the purchase.
        purchase_date (str): The date the purchase was made.
        purchase_amount (float): The amount of the purchase.
        purchase_status (str): The status of the purchase.
    """
    purchase_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String)
    software: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, server_default="Unpaid")
