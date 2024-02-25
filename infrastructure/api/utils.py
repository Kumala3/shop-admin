from typing import AsyncGenerator

from infrastructure.database.setup import create_engine, create_session_pool
from infrastructure.database.repo.requests import RequestsRepo

from config import load_config


config = load_config(".env")

engine = create_engine(config.db)
session_pool = create_session_pool(engine)


async def get_repo() -> AsyncGenerator[RequestsRepo, None]:
    async with session_pool() as session:
        yield RequestsRepo(session)
