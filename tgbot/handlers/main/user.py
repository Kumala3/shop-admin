from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from tgbot.keyboards.inline import menu_keyboard

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply(text="Вітаю, звичайний користувач!", reply_markup=menu_keyboard())
