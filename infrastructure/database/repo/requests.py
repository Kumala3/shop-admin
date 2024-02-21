from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repo.users import UserRepo
from infrastructure.database.repo.errors import ErrorRepo
from infrastructure.database.repo.features import FeatureRepo


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return UserRepo(self.session)

    @property
    def errors(self) -> ErrorRepo:
        """
        The Error repository sessions are required to manage error operations.
        """
        return ErrorRepo(self.session)

    @property
    def features(self) -> FeatureRepo:
        """
        The Features repository sessions are required to manage feature operations.
        """
        return FeatureRepo(self.session)
