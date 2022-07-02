import telebot
import datetime

from token_telegram import token


def send_notifications(time_respawn_ogre, time_respawn_robot):
    time_now = datetime.datetime.today()
    time_test = datetime.datetime(2022, 7, 1, 19, 1)
    ogre = time_respawn_ogre + datetime.timedelta(hours=23, minutes=1)
    robot = time_respawn_robot + datetime.timedelta(hours=26, minutes=1)
    print(time_test)
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
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}")

    @bot.message_handler(commands=['changetimezone'])
    def change_time_zone(message):
        bot.send_message(message.chat.id, "changetimezone")

    @bot.message_handler(commands=['spawn_robot'])
    def spawn_robot(message):
        spawn_robot = message.text
        time_spawn = spawn_robot.split(' ')
        time_spawn.pop(0)
        time_now = datetime.datetime.today()
        if (len(time_spawn)) != 4:
            bot.send_message(message.chat.id, "Данные введены некоректно, необходим формат: ЧАСЫ МИНУТЫ ДЕНЬ МЕСЯЦ")
        else:
            new_time_spawn = datetime.datetime(time_now.year, int(time_spawn[3]), int(time_spawn[2]),
                                               int(time_spawn[0]), int(time_spawn[1]))
            bot.send_message(message.chat.id, f"Спасибо за обновление, спавн робота был: {new_time_spawn}")

    @bot.message_handler(commands=['spawn_ogre'])
    def spawn_ogre(message):
        spawn_ogre = message.text
        time_spawn = spawn_ogre.split(' ')
        time_spawn.pop(0)
        time_now = datetime.datetime.today()
        if (len(time_spawn)) != 4:
            bot.send_message(message.chat.id, "Данные введены некоректно, необходим формат: ЧАСЫ МИНУТЫ ДЕНЬ МЕСЯЦ")
        else:
            new_time_spawn = datetime.datetime(time_now.year, int(time_spawn[3]), int(time_spawn[2]),
                                               int(time_spawn[0]), int(time_spawn[1]))
            bot.send_message(message.chat.id, f"Спасибо за обновление, спавн огра был: {new_time_spawn}")

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
            spawn_robot = message.text

            # time.strftime("%d")
            # bot.send_message(message.chat.id, "Неизвестная команда")
            # bot.send_message(message.chat.id, time)

    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)

    time_now = datetime.datetime.today()
    send_notifications(time_now, time_now)
