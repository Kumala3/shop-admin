from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from AaioAsync import AaioAsync

from tgbot.misc.async_session import get_session_pool
from tgbot.misc.states import SoftwareChoice, Tickets
from tgbot.keyboards.user_inline import UserKeyboards
from tgbot.misc.messages import UserMessages

from infrastructure.database.repo.requests import RequestsRepo
from config import Miscellaneous
from environs import Env

env = Env()
env.read_env()
miscelaneous = Miscellaneous.from_env(env)

user_router = Router()
aaio = AaioAsync(
    miscelaneous.api_key,
    miscelaneous.shop_id,
    miscelaneous.secretkey_1,
)


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.answer(
        text="Приветствую в нашем боте!", reply_markup=UserKeyboards.menu_keyboard()
    )


@user_router.callback_query(F.data == "translating")
async def buy_translating(query: CallbackQuery):
    await query.message.edit_text(
        text=UserMessages.buy_translate_text(),
        reply_markup=UserKeyboards.software_choices_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )


@user_router.callback_query(F.data.startswith("buy_"))
async def pay_order(query: CallbackQuery, state: FSMContext):
    data = query.data
    chosen_software = " ".join(data.split("_")[1:])

    async with get_session_pool() as session:
        repo = RequestsRepo(session)
        purchase = await repo.purchases.create_purchase(
            user_id=query.from_user.id,
            software=chosen_software,
            username=query.from_user.username,
        )

    link = await aaio.generatepaymenturl(
        amount=105,
        currency="RUB",
        desc=f"Покупка перевода для |{chosen_software}|{query.from_user.id}",
        order_id=purchase["purchase_id"],
    )

    await query.message.edit_text(
        text=UserMessages.payment_aaio(chosen_software),
        reply_markup=UserKeyboards.pay_with_link(link),
        parse_mode=ParseMode.MARKDOWN,
    )

    await state.set_state(SoftwareChoice.payment)


@user_router.callback_query(F.data == "back_pay_order")
async def back_pay_order(query: CallbackQuery):
    await query.message.edit_text(
        text=UserMessages.buy_translate_text(),
        reply_markup=UserKeyboards.software_choices_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )


@user_router.callback_query(F.data == "back_software_chs")
async def back_software_chs(query: CallbackQuery):
    await query.message.edit_text(
        text="Приветствую в нашем боте!", reply_markup=UserKeyboards.menu_keyboard()
    )


@user_router.callback_query(F.data == "offer_translate")
async def choose_offer_translate(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        text=UserMessages.choose_software_text(),
        reply_markup=UserKeyboards.available_softwares_fea_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(SoftwareChoice.software)


@user_router.callback_query(F.data == "report_error")
async def choose_soft_error(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(
        text=UserMessages.choose_software_text(),
        reply_markup=UserKeyboards.available_softwares_err_kb(),
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(SoftwareChoice.software)


@user_router.callback_query(F.data.startswith("err_"))
async def choose_software_error(query: CallbackQuery, state: FSMContext):
    data = query.data
    chosen_software = " ".join(data.split("_")[1:])

    await state.update_data(software=chosen_software)

    await query.message.edit_text(
        text=UserMessages.instruction_report_text(),
        reply_markup=UserKeyboards.back_keyboard("back_err_available"),
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(Tickets.error_message)


@user_router.callback_query(F.data.startswith("fea_"))
async def choose_software_feature(query: CallbackQuery, state: FSMContext):
    data = query.data
    chosen_software = " ".join(data.split("_")[1:])

    await state.update_data(software=chosen_software)

    await query.message.edit_text(
        text=UserMessages.instruction_feature_text(),
        reply_markup=UserKeyboards.back_keyboard("back_fea_available"),
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(Tickets.feature_message)


@user_router.callback_query(F.data.startswith("soft_back"))
async def back_chs_soft_error(query: CallbackQuery):
    if query.data == "soft_back_err_available":
        await query.message.edit_text(
            text=UserMessages.choose_software_text(),
            reply_markup=UserKeyboards.available_softwares_err_kb(),
            parse_mode=ParseMode.MARKDOWN,
        )
    elif query.data == "soft_back_fea_available":
        await query.message.edit_text(
            text=UserMessages.choose_software_text(),
            reply_markup=UserKeyboards.available_softwares_fea_kb(),
            parse_mode=ParseMode.MARKDOWN,
        )


@user_router.message(Tickets.error_message)
async def send_error_ticket(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    error_message = message.text

    data = await state.get_data()
    chosen_software = data.get("software")

    async with get_session_pool() as session:
        repo = RequestsRepo(session)
        await repo.errors.create_error_ticket(
            user_id=user_id,
            error_message=error_message,
            software=chosen_software,
            username=username,
        )

    await message.answer(text=UserMessages.confirm_request())

    await state.clear()


@user_router.message(Tickets.feature_message)
async def send_feature_ticket(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    error_message = message.text

    data = await state.get_data()
    chosen_software = data.get("software")

    async with get_session_pool() as session:
        repo = RequestsRepo(session)
        await repo.features.create_feature_ticket(
            user_id=user_id,
            feature_message=error_message,
            software=chosen_software,
            username=username,
        )

    await message.answer(text=UserMessages.confirm_request())

    await state.clear()


@user_router.message()
async def undefined_message(message: Message):
    await message.reply(
        text="Команда не найдена! Попробуйте вернуться в главное меню: /start"
    )
