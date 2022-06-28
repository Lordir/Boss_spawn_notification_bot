import telebot

from token import token


def telegram_bot(token):
    bot = telebot.TeleBot(token)
