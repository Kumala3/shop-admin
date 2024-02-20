from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext

from tgbot.misc.states import SoftwareChoice
from tgbot.keyboards.inline import UserKeyboards
from tgbot.misc.messages import Messages

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply(
        text="Приветствую в нашем боте!", reply_markup=UserKeyboards.menu_keyboard()
    )


@user_router.message()
async def undefined_message(message: Message):
    await message.reply(text="Команда не найдена! Попробуйте вернуться в главное меню: /start")


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

    await state.set_state(SoftwareChoice.chosen_software)
    await state.update_data(chosen_software=chosen_software)

    await query.message.edit_text(
        text=Messages.confirm_payment(chosen_software),
        reply_markup=UserKeyboards.pay_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )
    

@user_router.callback_query(F.data == "pay_order")
async def choose_payment(query: CallbackQuery):
    await query.message.edit_text(
        text="Выберите способ оплаты:", reply_markup=UserKeyboards.payments_keyboard()
    )


@user_router.callback_query(SoftwareChoice.chosen_software, F.data == "back_to_pay")
async def back_to_pay(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chosen_software = data.get("chosen_software")

    await query.message.edit_text(
        text=Messages.confirm_payment(chosen_software),
        reply_markup=UserKeyboards.pay_keyboard(),
        parse_mode=ParseMode.MARKDOWN,
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

