import telebot
import datetime
import asyncio
import aiohttp

from token_telegram import token, chat_id, moderators_id


# message.from_user.id

def send_notifications(bd_spawn_robot, bd_spawn_ogre):
    time_now = datetime.datetime.today()
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
    robot_hour = robot_datetime - datetime.timedelta(hours=1)
    robot_15_minutes = robot_datetime - datetime.timedelta(minutes=15)
    ogre_hour = ogre_datetime - datetime.timedelta(hours=1)
    ogre_15_minutes = ogre_datetime - datetime.timedelta(minutes=15)
    if time_now == robot_hour:
        pass
    elif time_now == robot_15_minutes:
        pass
    elif time_now == ogre_hour:
        pass
    elif time_now == ogre_15_minutes:
        pass
    elif (time_now.day == robot_datetime.day) and (time_now.hour == robot_datetime.hour) and (
            time_now.minute == robot_datetime.minute):
        robot_new = robot_datetime + datetime.timedelta(hours=26, minutes=1)
        time_write = datetime.datetime(time_now.year, robot_new.month, robot_new.day,
                                       robot_new.hour, robot_new.minute)
        bd = open('bd_spawn_robot.txt', 'a')
        bd.write("bot =" + str(time_write) + '\n')
        bd.close()
    elif (time_now.day == ogre_datetime.day) and (time_now.hour == ogre_datetime.hour) and (
            time_now.minute == ogre_datetime.minute):
        ogre_new = ogre_datetime + datetime.timedelta(hours=23, minutes=1)
        time_write = datetime.datetime(time_now.year, ogre_new.month, ogre_new.day,
                                       ogre_new.hour, ogre_new.minute)
        bd = open('bd_spawn_ogre.txt', 'a')
        bd.write("bot =" + str(time_write) + '\n')
        bd.close()


bot = telebot.TeleBot(token)


def telegram_bot(bd_spawn_robot, bd_spawn_ogre):

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
                robot_new = new_time_spawn + datetime.timedelta(hours=26, minutes=1)
                bot.send_message(message.chat.id, f"Спасибо за обновление, следующий спавн робота: {robot_new}")
                bd = open('bd_spawn_robot.txt', 'a')
                bd.write(message.from_user.first_name + ' =' + str(robot_new) + '\n')
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
                ogre_new = new_time_spawn + datetime.timedelta(hours=23, minutes=1)
                bot.send_message(message.chat.id, f"Спасибо за обновление, следующий спавн огра: {ogre_new}")
                bd = open('bd_spawn_ogre.txt', 'a')
                bd.write(message.from_user.first_name + ' =' + str(ogre_new) + '\n')
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

    # bot.polling()


if __name__ == '__main__':
    bd_spawn_robot = open('bd_spawn_robot.txt', 'r')
    bd_spawn_ogre = open('bd_spawn_ogre.txt', 'r')
    # send_notifications(bd_spawn_robot, bd_spawn_ogre)
    telegram_bot(bd_spawn_robot, bd_spawn_ogre)
    bot.polling(none_stop=True)

    time_now = datetime.datetime.today()
    send_notifications(time_now, time_now)
