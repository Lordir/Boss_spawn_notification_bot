import telebot

from token_telegram import token


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "Hello")

    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
