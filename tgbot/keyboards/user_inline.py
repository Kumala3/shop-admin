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
            text="🐸 Перевод для SF SEO Spider 19.4",
            callback_data="buy_SF_SEO_Spider_19.4",
        )
        keyboard.button(
            text="🐸 Перевод для SF SEO Spider 19.2",
            callback_data="buy_SF_SEO_Spider_19.2",
        )
        keyboard.button(
            text="🐸 Перевод для SF Log File Analyser 6.0",
            callback_data="buy_SF_Log_File_Analyser_6.0",
        )
        keyboard.button(
            text="🐸 Перевод для SF Log File Analyser 5.3",
            callback_data="buy_SF_Log_File_Analyser_5.3",
        )
        keyboard.button(
            text="Показать оферту",
            url="https://drive.google.com/file/d/1NRTagfkSdYenybyCiOMB-BqgYWCPsblv/view?usp=drive_link",
        )
        keyboard.button(text="🔙 Назад", callback_data="back_software_chs")

        keyboard.adjust(1)

        return keyboard.as_markup()

    def available_softwares_err_kb():
        keyboard = InlineKeyboardBuilder()

        keyboard.button(
            text="🐸 SF SEO Spider 19.4", callback_data="err_SF_SEO_Spider_19.4"
        )
        keyboard.button(
            text="🐸 SF SEO Spider 19.2", callback_data="err_SF_SEO_Spider_19.2"
        )
        keyboard.button(
            text="🐸 SF Log File Analyser 6.0",
            callback_data="err_SF_Log_File_Analyser_6.0",
        )
        keyboard.button(
            text="🐸 SF Log File Analyser 5.3",
            callback_data="err_SF_Log_File_Analyser_5.3",
        )
        keyboard.button(text="🔙 Назад", callback_data="back_software_chs")

        keyboard.adjust(1)

        return keyboard.as_markup()

    def available_softwares_fea_kb():
        keyboard = InlineKeyboardBuilder()

        keyboard.button(
            text="🐸 SF SEO Spider 19.4", callback_data="fea_SF_SEO_Spider_19.4"
        )
        keyboard.button(
            text="🐸 SF SEO Spider 19.2", callback_data="fea_SF_SEO_Spider_19.2"
        )
        keyboard.button(
            text="🐸 SF Log File Analyser 6.0",
            callback_data="fea_SF_Log_File_Analyser_6.0",
        )
        keyboard.button(
            text="🐸 SF Log File Analyser 5.3",
            callback_data="fea_SF_Log_File_Analyser_5.3",
        )
        keyboard.button(text="🔙 Назад", callback_data="back_software_chs")

        keyboard.adjust(1)

        return keyboard.as_markup()

    def back_keyboard(path: str):
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text="🔙 Назад", callback_data=f"soft_{path}")

        return keyboard.as_markup()

    def pay_keyboard():
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text="💳 Оплатить", callback_data="pay_order")
        keyboard.button(text="🔙 Назад", callback_data="back_pay_order")

        return keyboard.as_markup()

    def pay_with_link(link: str):
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text="💳 Оплатить", url=link)
        keyboard.button(text="🔙 Назад", callback_data="back_pay_order")

        return keyboard.as_markup()

    def payments_keyboard():
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text="💳 Cards/Crypto/QIWI", callback_data="pay")
        keyboard.button(text="🔙 Назад", callback_data="back_to_pay")

        keyboard.adjust(1)

        return keyboard.as_markup()
