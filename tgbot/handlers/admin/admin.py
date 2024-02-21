from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.admin_inline import AdminKeyboard
from tgbot.misc.messages import AdminMessages

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.answer(
        text=AdminMessages.greet_admin(),
        reply_markup=AdminKeyboard.show_main_menu(),
        parse_mode=ParseMode.MARKDOWN,
    )
