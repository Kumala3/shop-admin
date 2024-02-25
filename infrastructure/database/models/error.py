from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BIGINT, String, ForeignKey

from .base import Base, TableNameMixin, TimestampMixin


class Error(Base, TableNameMixin, TimestampMixin):
    """
    Represents an error ticket associated with translate.

    Attributes:
        error_id (int): The ID of the error ticket.
        user_id (int): The ID of the user associated with the error.
        username (str, optional): The username of the user associated with the error.
        error_message (str): The error message.
        status (str): The status of the error. Defaults to "New".
        software (str): The software where the error was detected.
    """
    error_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"), nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String)
    error_message: Mapped[str] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(String, server_default="New")
    software: Mapped[str] = mapped_column(String)
