from aiogram.utils.keyboard import InlineKeyboardBuilder


class UserKeyboards:
    def menu_keyboard():
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text="💳 Купить перевод", callback_data="translating")
        keyboard.button(
            text="⚠️ Сообщить об ошибке перевода", callback_data="report_error"
        )
        keyboard.button(
            text="💡 Написать пожелание / предложить свой перевод",
            callback_data="offer_translate",
        )

        keyboard.adjust(1)

        return keyboard.as_markup()

    def software_choices_kb():
        keyboard = InlineKeyboardBuilder()

        keyboard.button(
            text="🐸 Перевод для SF SEO Spider 19.4", callback_data="buy_spider_19.4"
        )
        keyboard.button(
            text="🐸 Перевод для SF SEO Spider 19.2", callback_data="buy_spider_19.2"
        )
        keyboard.button(
            text="🐸 Перевод для SF Log File Analyser 6.0", callback_data="buy_analyser_6.0"
        )
        keyboard.button(
            text="🐸 Перевод для SF Log File Analyser 5.3", callback_data="buy_analyser_5.3"
        )
        keyboard.button(text="🔙 Назад", callback_data="back_software_chs")

        keyboard.adjust(1)

        return keyboard.as_markup()

    def software_error_kb():
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text="🐸 SF SEO Spider 19.4", callback_data="err_spider_19.4")
        keyboard.button(text="🐸 SF SEO Spider 19.2", callback_data="err_spider_19.2")
        keyboard.button(
            text="🐸 SF Log File Analyser 6.0", callback_data="err_analyser_6.0"
        )
        keyboard.button(
            text="🐸 SF Log File Analyser 5.3", callback_data="err_analyser_5.3"
        )
        keyboard.button(text="🔙 Назад", callback_data="back_software_chs")

        keyboard.adjust(1)

        return keyboard.as_markup()

    def back_keyboard(path: str):
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text="🔙 Назад", callback_data=f"back_{path}")

        return keyboard.as_markup()

    def pay_keyboard():
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text="💳 Оплатить", callback_data="pay")
        keyboard.button(text="🔙 Назад", callback_data="back_pay")

        return keyboard.as_markup()
