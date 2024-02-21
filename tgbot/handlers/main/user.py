from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext

from tgbot.misc.states import SoftwareChoice, ErrorMessage
from tgbot.keyboards.inline import UserKeyboards
from tgbot.misc.messages import Messages
from config import load_config

from infrastructure.database.setup import create_engine, create_session_pool
from infrastructure.database.repo.requests import RequestsRepo

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply(
        text="Приветствую в нашем боте!", reply_markup=UserKeyboards.menu_keyboard()
    )


@user_router.callback_query(F.data == "translating")
async def buy_translating(query: CallbackQuery):
    await query.message.edit_text(
        text=Messages.buy_translate_text(),
        reply_markup=UserKeyboards.software_choices_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )


@user_router.callback_query(F.data.startswith("buy_"))
async def pay_order(query: CallbackQuery, state: FSMContext):
    data = query.data
    chosen_software = " ".join(data.split("_")[1:])

    await state.set_state(SoftwareChoice.software)
    await state.update_data(software=chosen_software)

    await query.message.edit_text(
        text=Messages.confirm_payment(chosen_software),
        reply_markup=UserKeyboards.pay_keyboard(),
        parse_mode=ParseMode.MARKDOWN,
    )


@user_router.callback_query(SoftwareChoice.software, F.data == "back_to_pay")
async def back_to_pay(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chosen_software = data.get("chosen_software")

    await query.message.edit_text(
        text=Messages.confirm_payment(chosen_software),
        reply_markup=UserKeyboards.pay_keyboard(),
        parse_mode=ParseMode.MARKDOWN,
    )


@user_router.callback_query(F.data == "pay_order")
async def choose_payment(query: CallbackQuery):
    await query.message.edit_text(
        text="Выберите способ оплаты:", reply_markup=UserKeyboards.payments_keyboard()
    )


@user_router.callback_query(F.data == "back_pay_order")
async def back_pay_order(query: CallbackQuery):
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
async def choose_soft_error(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        text=Messages.report_error_text(),
        reply_markup=UserKeyboards.software_error_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(SoftwareChoice.software)


@user_router.callback_query(F.data == "back_chs_report")
async def back_chs_soft_error(query: CallbackQuery):
    await query.message.edit_text(
        text=Messages.report_error_text(),
        reply_markup=UserKeyboards.software_error_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )


@user_router.callback_query(F.data.startswith("err_"))
async def report_message(query: CallbackQuery, state: FSMContext):
    data = query.data
    chosen_software = " ".join(data.split("_")[1:])

    await state.update_data(software=chosen_software)

    await query.message.edit_text(
        text=Messages.instruction_report_text(),
        reply_markup=UserKeyboards.back_keyboard("chs_report"),
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(ErrorMessage.error_message)


@user_router.message(ErrorMessage.error_message)
async def catch_message(message: Message, state: FSMContext):
    config = load_config(".env")

    engine = create_engine(config.db)
    session_pool = create_session_pool(engine)

    user_id = message.from_user.id
    username = message.from_user.username
    error_message = message.text

    data = await state.get_data()
    chosen_software = data.get("software")

    async with session_pool() as session:
        repo = RequestsRepo(session)
        await repo.errors.create_error_ticket(
            user_id=user_id,
            error_message=error_message,
            software=chosen_software,
            username=username,
        )

    await message.answer(
        text=Messages.confirm_request()
    )


@user_router.message()
async def undefined_message(message: Message):
    await message.reply(
        text="Команда не найдена! Попробуйте вернуться в главное меню: /start"
    )
