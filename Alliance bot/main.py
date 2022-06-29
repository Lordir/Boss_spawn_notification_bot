import telebot

from token_telegram import token


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}"
                                          f" Укажи свой часовой пояс"
                                          f" (Необходимо ввести цифру и знак, обозначающие разницу времени от мск."
                                          f" Например, +4)")

    @bot.message_handler()
    def get_user_text(message):
        if message.text == ("+" + "1"):
            bot.send_message(message.chat.id, f"Ваш часовой пояс = {message.text}")
        elif message.text == ("-" + "1"):
            bot.send_message(message.chat.id, f"Ваш часовой пояс = {message.text}")
        else:
            bot.send_message(message.chat.id, "Неизвестная команда")

    @bot.message_handler(commands=['changetimezone'])
    def change_time_zone(message):
        bot.send_message(message.chat.id, "changetimezone")

    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
