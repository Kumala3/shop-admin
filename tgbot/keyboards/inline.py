from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="💳 Купить перевод", callback_data="buy_translate")
    keyboard.button(text="⚠️ Сообщить об ошибке перевода", callback_data="report_error")
    keyboard.button(
        text="💡 Написать пожелание / предложить свой перевод",
        callback_data="offer_translate",
    )

    keyboard.adjust(1)

    return keyboard.as_markup()
