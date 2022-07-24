import telebot
import datetime

from token_telegram import token, chat_id, moderators_id


# message.from_user.id

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
    bd_spawn_robot = open('bd_spawn_robot.txt', 'r')
    bd_spawn_ogre = open('bd_spawn_ogre.txt', 'r')
    last_spawn_robot = bd_spawn_robot.readlines()[-1]
    last_spawn_ogre = bd_spawn_ogre.readlines()[-1]
    # remove_last удаляет /n в конце строки
    remove_last_robot = last_spawn_robot[:-1]
    remove_last_ogre = last_spawn_ogre[:-1]
    # Благодаря split разделяется имя пользователя и сама дата, после чего имя удаляется, остается только дата
    time_robot = remove_last_robot.split('=')
    time_robot.pop(0)
    time_ogre = remove_last_ogre.split('=')
    time_ogre.pop(0)
    print(time_robot)
    print(time_ogre)
    # Преобразование даты из str в datetime
    robot_datetime = datetime.datetime.strptime(time_robot[0], '%Y-%m-%d %H:%M:%S')
    ogre_datetime = datetime.datetime.strptime(time_ogre[0], '%Y-%m-%d %H:%M:%S')
    # Рассчет следующего спавна
    robot = robot_datetime + datetime.timedelta(hours=26, minutes=1)
    ogre = ogre_datetime + datetime.timedelta(hours=23, minutes=1)
    # Оповещения
    # r_hour = ""
    print(robot)
    time_now = datetime.datetime.today()
    print(time_now)
    print((time_now - robot).seconds)
    if (time_now - robot).seconds < 3600:
        # if r_hour != time_now.day:
        #     r_hour = time_now.day
        bot.send_message(chat_id, "Спавн робота через час")
        print("Спавн робота через час")
    elif (time_now - robot).seconds < 900:
        print("Спавн робота 15 минут")
    if (time_now - ogre).seconds < 3600:
        print("Спавн огра через час")
    elif (time_now - ogre).seconds < 900:
        print("Спавн огра 15 минут")

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}")

    @bot.message_handler(commands=['changetimezone'])
    def change_time_zone(message):
        bot.send_message(message.chat.id, "changetimezone")

    @bot.message_handler(commands=['spawn_robot'])
    def spawn_robot(message):
        if message.from_user.id in moderators_id:
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
                bd = open('bd_spawn_robot.txt', 'a')
                bd.write(message.from_user.first_name + ' =' + str(new_time_spawn) + '\n')
                bd.close()
        else:
            bot.send_message(message.chat.id, "Вы не имеете прав для обновления спавна босса")

    @bot.message_handler(commands=['spawn_ogre'])
    def spawn_ogre(message):
        if message.from_user.id in moderators_id:
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
                bd = open('bd_spawn_ogre.txt', 'a')
                bd.write(message.from_user.first_name + ' =' + str(new_time_spawn) + '\n')
                bd.close()
        else:
            bot.send_message(message.chat.id, "Вы не имеете прав для обновления спавна босса")

    @bot.message_handler()
    def get_user_text(message):
        if message.text == ("+" + "1"):
            bot.send_message(message.chat.id, f"Ваш часовой пояс = {message.text}")
            # bot.send_message(message.chat.id, message.from_user.id)
            # bot.send_message(message.chat.id, message)
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
