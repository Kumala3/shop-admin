from aiogram.utils.markdown import bold


class UserMessages:
    def buy_translate_text():
        text = f"""
        
{bold("Дополнительная информация:")}
1. {bold("Переводы работают только для платформы WINDOWS;")}
2. Не смотря на то, что переводы сделаны отдельным файлом, в интерфейсе программ не будет отдельного селекта с RU языком. Все потому, что это настраивается где-то в файлах Java, поэтому реализовать это не получиться;
3. В интерфейсе программ будут встречаться непереведенные фрагменты текста. Это не потому что перевод не полный, а потому что эти фрагменты подгружаются из файлов Java и изменить их также не получиться;
4. При покупке перевода, все пользователи будут получать обновление текущей версии программы. Если вы купили перевод для версии SF SEO Spider 19.4, то вы бесплатно получите перевод для версий 19.5, 19.6 и т.д. Для версии SF SEO Spider 20.0 потребуется повторная покупка перевода;

{bold("Стоимость переводов:")}
• SF SEO Spider 19.4 — 105 рублей или 1 USDT TRC20;
• SF SEO Spider 19.2 — 105 рублей или 1 USDT TRC20;
• SF Log File Analyser 6.0 — 105 рублей или 1 USDT TRC20;
• SF Log File Analyser 5.3 — 105 рублей или 1 USDT TRC20;

Перед покупкой прочтите договор публичной оферты 👇
        """

        return text.replace("\\", "")

    def choose_software_text():
        return f"""{bold("Выберите версию программы:")}
• SF SEO Spider 19.4
• SF SEO Spider 19.2
• SF Log File Analyser 6.0
• SF Log File Analyser 5.3
"""

    def payment_aaio(chosen_software: str):
        text = f"""Вы хотите оплатить перевод для {bold(chosen_software)}.\n Используйте кнопку ниже для оплаты:""" 
        return text.replace("\\", "")

    def instruction_report_text():
        text = f"""{bold("Пожалуйста, напишите в произвольной форме где вы нашли ошибку и по возможности сделайте скриншот в виде ссылки.")}"""

        return text.replace("\\", "")

    def instruction_feature_text():
        text = f"""{bold("Пожалуйста, напишите в произвольной форме свои предложения по улучшению перевода и по возможности сделайте скриншот в виде ссылки.")}"""
        return text.replace("\\", "")

    def confirm_payment(chosen_software: str):
        text = f"""Вы выбрали перевод для {bold(chosen_software)}. Для оплаты нажмите кнопку «Оплатить»"""
        return text.replace("\\", "")

    def confirm_request():
        return "Спасибо за обращение! Оно будет рассмотрено в ближайшее время."


class AdminMessages:
    def greet_admin():
        text = f"""{bold("Приветствую Админ! Выберете действие:")}"""
        return text.replace("\\", "")
