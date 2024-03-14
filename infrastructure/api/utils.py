import logging
import betterlogging as bl

import os
from typing import AsyncGenerator

from infrastructure.database.setup import create_engine, create_session_pool
from infrastructure.database.repo.requests import RequestsRepo

from config import load_config
from bot import bot
from aiogram.types.input_file import BufferedInputFile

config = load_config(".env")

engine = create_engine(config.db)
session_pool = create_session_pool(engine)

log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)


async def get_repo() -> AsyncGenerator[RequestsRepo, None]:
    async with session_pool() as session:
        yield RequestsRepo(session)


async def send_file(user_ids: list, message: str, file_path: str):
    try:
        # Reading the file as bytes-object and sending it to the user
        with open(file_path, "rb") as file:
            file_content = file.read()
            for user_id in user_ids:
                await bot.send_document(
                    user_id,
                    document=BufferedInputFile(file_content, filename=file_path),
                    caption=message,
                )
        log.info(f"File was sent to {len(user_ids)} users")
    except Exception as e:
        log.info(f"Error sending file to user {user_id}: {e}")
    try:
        # When we have already sent the file, we can delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info(f"File: {file_path} was successfully deleted")
    except Exception as e:
        log.info(f"Error deleting file: {e}")


async def send_message(message: str, users_ids: list):
    try:
        # Send the message to all users by user_id
        for user_id in users_ids:
            try:
                await bot.send_message(
                    user_id, text=message, disable_web_page_preview=True
                )
            except Exception as e:
                log.info(f"Error sending message to user {user_id}: {e}")
        log.info(f"Mailing was successful for {len(users_ids)} users")
    except Exception as e:
        log.info(f"Error sending message: {e}")
