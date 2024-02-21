from aiogram.utils.keyboard import InlineKeyboardBuilder


class AdminKeyboard:
    def show_main_menu():
        keyboard = InlineKeyboardBuilder()

        keyboard.button(text="📊 Статистика", callback_data="stats")
        keyboard.button(text="📝 Analyze tickets", callback_data="analyze_tickets")
        keyboard.button(text="📧 Mailing", callback_data="mailing")

        keyboard.adjust(1)

        return keyboard.as_markup()

