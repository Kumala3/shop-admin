import logging
import betterlogging as bl

from typing import AsyncGenerator

from infrastructure.database.setup import create_engine, create_session_pool
from infrastructure.database.repo.requests import RequestsRepo

from config import load_config
from aiohttp import ClientSession, FormData

config = load_config(".env")

engine = create_engine(config.db)
session_pool = create_session_pool(engine)

log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)

async def get_repo() -> AsyncGenerator[RequestsRepo, None]:
    async with session_pool() as session:
        yield RequestsRepo(session)


async def get_file_url(file_path: str):
    url = "https://uguu.se/upload"
    data = FormData()
    data.add_field("files[]", open(file_path, "rb"))

    async with ClientSession() as session:
        async with session.post(url=url, data=data) as response:
            if response.status == 200:
                response_json = await response.json()
                upload_url = response_json.get("files")[0].get("url")

                if upload_url:
                    return upload_url
                else:
                    log.info("Failed to get the upload URL from the response.")
                    return None
            else:
                log.info(f"Failed to upload file. Status code: {response.status}")
                return None
