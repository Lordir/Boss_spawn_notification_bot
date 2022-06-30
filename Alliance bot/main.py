import telebot
import datetime

from token_telegram import token


def send_notifications(time_respawn_ogre, time_respawn_robot):
    time_now = datetime.datetime.today()
    time_test = datetime.datetime(2022, 7, 1, 19, 1)
    ogre = time_respawn_ogre + datetime.timedelta(hours=23, minutes=1)
    robot = time_respawn_robot + datetime.timedelta(hours=26, minutes=1)
    # print(time_test)
    # print(ogre)

    # time_test.strftime()

    if (ogre - time_test).seconds < 3600:
        print("Спавн огра через час")
    elif (ogre - time_test).seconds < 900:
        print("Спавн огра 15 минут")
    if (robot - time_test).seconds < 3600:
        print("Спавн робота через час")
    elif (robot - time_test).seconds < 900:
        print("Спавн робота 15 минут")


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
            # a = datetime.datetime.today()
            # ogre = a + datetime.timedelta(hours=23, minutes=1)
            # robot = a + datetime.timedelta(hours=26, minutes=1)
            # bot.send_message(message.chat.id, a)
            # bot.send_message(message.chat.id, ogre)
            # bot.send_message(message.chat.id, robot)
            bot.send_message(message.chat.id, "Неизвестная команда")

    @bot.message_handler(commands=['changetimezone'])
    def change_time_zone(message):
        bot.send_message(message.chat.id, "changetimezone")

    @bot.message_handler(commands=['spawn_robot'])
    def spawn_robot(message):
        pass

    @bot.message_handler(commands=['spawn_ogre'])
    def spawn_ogre(message):
        pass

    bot.polling()


if __name__ == '__main__':
    # telegram_bot(token)

    time_now = datetime.datetime.today()
    send_notifications(time_now, time_now)
