from datetime import datetime

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func
from typing_extensions import Annotated

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class TableNameMixin:
    """
    Mixin class that provides a default implementation for generating the table name based on the class name.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Returns the table name for the class.

        Returns:
            str: The table name.
        """
        return cls.__name__.lower() + "s"


class TimestampMixin:
    """
    A mixin class that provides timestamp functionality for database models.
    """

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now())
