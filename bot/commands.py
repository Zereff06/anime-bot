from config import *
from aiogram.types import Message
from buttons import b_main_menu
from buttons.find_anime import show_last_10_anime
from utilities import sql






"""Commands"""
# Команда подписки
@dp.message_handler(commands = ['hello','hi'])
async def hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await sql.create_user(message)
    await message.answer('Рады вас видеть!\nДля начала работы с ботом, введите /menu и выберите нужные фильтры.')


@dp.message_handler(commands=['menu'])
async def start(message: Message):
    await b_main_menu.start(message)




"""Utils"""
# Ответ на неузнаную команду
@dp.message_handler()
async def echo( message: Message ):
    sql_user = await sql.get_user_and_add_log(message)

    if await b_main_menu.chek(sql_user, message):
        return
    elif await show_last_10_anime.check(message):
        return
    else:
        await message.answer('К сожалению, я тебя не понял :с')








