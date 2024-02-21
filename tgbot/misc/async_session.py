from sqlalchemy.ext.asyncio import AsyncSession
from config import load_config

from infrastructure.database.setup import create_engine, create_session_pool


def get_session_pool() -> AsyncSession:
    config = load_config(".env")

    engine = create_engine(config.db)
    session_pool = create_session_pool(engine)

    return session_pool()

