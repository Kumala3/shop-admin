from typing import Optional

from sqlalchemy import Integer, BIGINT, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TableNameMixin, TimestampMixin


class Feature(Base, TableNameMixin, TimestampMixin):
    """
    Represents a feature ticket associated with new innovations to translate.

    Attributes:
        feature_id (int): The unique identifier for the feature.
        user_id (int): The user ID associated with the feature.
        username (str, optional): The username associated with the feature.
        feature_message (str): The message describing the feature.
        status (str): The status of the feature (default is "New").
        software (str): The software associated with the feature.
    """
    feature_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String)
    feature_message: Mapped[str] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(String, server_default="New")
    software: Mapped[str] = mapped_column(String)

