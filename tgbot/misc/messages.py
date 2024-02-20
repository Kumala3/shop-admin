from aiogram.utils.markdown import bold


class Messages:
    def buy_translate_text():
        text = f"""{bold("ВАЖНО! Переводы работают только для платформы WINDOWS!")}

Стоимость переводов:
• SF SEO Spider 19.4 — 95 рублей или 1 USDT TRC20;
• SF SEO Spider 19.2 — 95 рублей или 1 USDT TRC20;
• SF Log File Analyser 6.0 — 95 рублей или 1 USDT TRC20;
• SF Log File Analyser 5.3 — 95 рублей или 1 USDT TRC20;
        """

        return text.replace("\\", "")

    def report_error_text():
        return f"""{bold("Выберите версию программы:")}
• SF SEO Spider 19.4
• SF SEO Spider 19.2
• SF Log File Analyser 6.0
• SF Log File Analyser 5.3
"""

    def instruction_report_text():
        text = f"""{bold("Пожалуйста, напишите в произвольной форме где вы нашли ошибку и по возможности сделайте скриншот в виде ссылки.")}"""

        return text.replace("\\", "")
