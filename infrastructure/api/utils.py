import logging
import betterlogging as bl

from typing import AsyncGenerator

from infrastructure.database.setup import create_engine, create_session_pool
from infrastructure.database.repo.requests import RequestsRepo

from config import load_config
import aiohttp

config = load_config(".env")

engine = create_engine(config.db)
session_pool = create_session_pool(engine)

log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)

async def get_repo() -> AsyncGenerator[RequestsRepo, None]:
    async with session_pool() as session:
        yield RequestsRepo(session)


async def upload_file_to_temp_storage(file_path: str):
    url = "https://tmpfiles.org/api/v1/upload"

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=file_path) as response:
            if response.status == 200:
                response_json = response.json()
                upload_url = response_json.get("url")

                if upload_url:
                    log.info(f"File uploaded successfully! URL: {upload_url}")
                else:
                    log.info("Failed to get the upload URL from the response.")
            else:
                log.info(f"Failed to upload file. Status code: {response.status}")
