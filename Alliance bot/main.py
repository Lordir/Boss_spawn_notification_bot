import logging
import datetime

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from token_telegram import token, chat_id, moderators_id

# Configure logging
logging.basicConfig(level=logging.INFO)

# message.from_user.id

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)


async def send_notifications():
    while True:
        bd_spawn_robot = open('bd_spawn_robot.txt', 'r')
        bd_spawn_ogre = open('bd_spawn_ogre.txt', 'r')
        loop = asyncio.get_event_loop()
        loop.create_task(check_time(bd_spawn_robot, bd_spawn_ogre))
        # check_time(bd_spawn_robot, bd_spawn_ogre)
        await asyncio.sleep(60)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(f"Hello, {message.from_user.first_name}")


@dp.message_handler(commands=['spawn_robot'])
async def spawn_robot(message: types.Message):
    if message.from_user.id in moderators_id:
        spawn_robot = message.text
        time_spawn = spawn_robot.split(' ')
        time_spawn.pop(0)
        time_now = datetime.datetime.today()
        if (len(time_spawn)) != 4:
            await message.reply("Данные введены некоректно, необходим формат: ЧАСЫ МИНУТЫ ДЕНЬ МЕСЯЦ")
        else:
            new_time_spawn = datetime.datetime(time_now.year, int(time_spawn[3]), int(time_spawn[2]),
                                               int(time_spawn[0]), int(time_spawn[1]))
            robot_new = new_time_spawn + datetime.timedelta(hours=26, minutes=1)
            await message.reply(f"Спасибо за обновление, следующий спавн робота: {robot_new}")
            bd = open('bd_spawn_robot.txt', 'a')
            bd.write(message.from_user.first_name + ' =' + str(robot_new) + '\n')
            bd.close()
    else:
        await message.reply("Вы не имеете прав для обновления спавна босса")


@dp.message_handler(commands=['spawn_ogre'])
async def spawn_ogre(message: types.Message):
    if message.from_user.id in moderators_id:
        spawn_ogre = message.text
        time_spawn = spawn_ogre.split(' ')
        time_spawn.pop(0)
        time_now = datetime.datetime.today()
        if (len(time_spawn)) != 4:
            await message.reply("Данные введены некоректно, необходим формат: ЧАСЫ МИНУТЫ ДЕНЬ МЕСЯЦ")
        else:
            new_time_spawn = datetime.datetime(time_now.year, int(time_spawn[3]), int(time_spawn[2]),
                                               int(time_spawn[0]), int(time_spawn[1]))
            ogre_new = new_time_spawn + datetime.timedelta(hours=23, minutes=1)
            await message.reply(f"Спасибо за обновление, следующий спавн огра: {ogre_new}")
            bd = open('bd_spawn_ogre.txt', 'a')
            bd.write(message.from_user.first_name + ' =' + str(ogre_new) + '\n')
            bd.close()
    else:
        await message.reply("Вы не имеете прав для обновления спавна босса")


@dp.message_handler()
async def get_user_text(message: types.Message):
    await message.reply("Неизвестная команда")


async def check_time(bd_spawn_robot, bd_spawn_ogre):
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
    # print(time_robot)
    # print(time_ogre)
    # Преобразование даты из str в datetime
    robot_datetime = datetime.datetime.strptime(time_robot[0], '%Y-%m-%d %H:%M:%S')
    ogre_datetime = datetime.datetime.strptime(time_ogre[0], '%Y-%m-%d %H:%M:%S')
    robot_hour = robot_datetime - datetime.timedelta(hours=1)
    robot_15_minutes = robot_datetime - datetime.timedelta(minutes=15)
    ogre_hour = ogre_datetime - datetime.timedelta(hours=1)
    ogre_15_minutes = ogre_datetime - datetime.timedelta(minutes=15)
    if (time_now.day == robot_hour.day) and (time_now.hour == robot_hour.hour) and (
            time_now.minute == robot_hour.minute):
        await bot.send_message(chat_id, "Спавн робота через час")
    elif (time_now.day == robot_15_minutes.day) and (time_now.hour == robot_15_minutes.hour) and (
            time_now.minute == robot_15_minutes.minute):
        await bot.send_message(chat_id, "Спавн робота через 15 минут")
    elif (time_now.day == ogre_hour.day) and (time_now.hour == ogre_hour.hour) and (
            time_now.minute == ogre_hour.minute):
        await bot.send_message(chat_id, "Спавн огра через час")
    elif (time_now.day == ogre_15_minutes.day) and (time_now.hour == ogre_15_minutes.hour) and (
            time_now.minute == ogre_15_minutes.minute):
        await bot.send_message(chat_id, "Спавн огра через 15 минут")
    elif (time_now.day == robot_datetime.day) and (time_now.hour == robot_datetime.hour) and (
            time_now.minute == robot_datetime.minute):
        robot_new = robot_datetime + datetime.timedelta(hours=26, minutes=1)
        time_write = datetime.datetime(time_now.year, robot_new.month, robot_new.day,
                                       robot_new.hour, robot_new.minute)
        bd = open('bd_spawn_robot.txt', 'a')
        bd.write("bot =" + str(time_write) + '\n')
        bd.close()
        await bot.send_message(chat_id, f"Робот заспавнился, следующий спавн: {robot_new}")
    elif (time_now.day == ogre_datetime.day) and (time_now.hour == ogre_datetime.hour) and (
            time_now.minute == ogre_datetime.minute):
        ogre_new = ogre_datetime + datetime.timedelta(hours=23, minutes=1)
        time_write = datetime.datetime(time_now.year, ogre_new.month, ogre_new.day,
                                       ogre_new.hour, ogre_new.minute)
        bd = open('bd_spawn_ogre.txt', 'a')
        bd.write("bot =" + str(time_write) + '\n')
        bd.close()
        await bot.send_message(chat_id, f"Огр заспавнился, следующий спавн: {ogre_new}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_notifications())
    executor.start_polling(dp, skip_updates=True)
