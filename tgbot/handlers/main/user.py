from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode

from tgbot.misc.states import SoftWareChoice
from tgbot.keyboards.inline import UserKeyboards
from tgbot.misc.messages import Messages

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply(
        text="Вітаю, звичайний користувач!", reply_markup=UserKeyboards.menu_keyboard()
    )


@user_router.message()
async def undefined_message(message: Message):
    await message.reply(text="Я не розумію, що ти хочеш.")


@user_router.callback_query(F.data == "translating")
async def buy_translating(query: CallbackQuery):
    await query.message.edit_text(
        text=Messages.buy_translate_text(),
        reply_markup=UserKeyboards.software_choices_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )

@user_router.callback_query(F.data == "back_software_chs")
async def back_software_chs(query: CallbackQuery):
    await query.message.edit_text(
        text="Вітаю, звичайний користувач!", reply_markup=UserKeyboards.menu_keyboard()
    )


@user_router.callback_query((F.data == "report_error") | (F.data == "offer_translate"))
async def choose_soft_error(query: CallbackQuery):
    await query.message.edit_text(
        text=Messages.report_error_text(),
        reply_markup=UserKeyboards.software_error_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )


@user_router.callback_query(F.data == "back_chs_report")
async def back_chs_soft_error(query: CallbackQuery):
    await query.message.edit_text(
        text=Messages.report_error_text(),
        reply_markup=UserKeyboards.software_error_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )


@user_router.callback_query(F.data.startswith("err_"))
async def report_message(query: CallbackQuery):
    await query.message.edit_text(
        text=Messages.instruction_report_text(),
        reply_markup=UserKeyboards.back_keyboard("chs_report"),
        parse_mode=ParseMode.MARKDOWN,
    )

