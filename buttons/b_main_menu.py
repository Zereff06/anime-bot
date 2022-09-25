from config import *
from aiogram import types

from buttons.find_anime import b_find_anime
from buttons.playlist import b_playlist
from buttons.settings import  b_settings






async def start( message: types.Message ):
    button_menu = types.ReplyKeyboardMarkup(resize_keyboard = False)
    button_menu.add(types.InlineKeyboardButton("Найти аниме"))
    button_menu.add(types.InlineKeyboardButton("Мой плейлист"))
    # button_menu.add(types.InlineKeyboardButton("Настройки"))

    await message.answer("Главное меню:", reply_markup = button_menu)






async def chek(sql_user, message: types.Message ):
    text = message.text.lower()

    if text == 'главное меню':
        await start(message)
        return True


    elif text == 'найти аниме':
         await b_find_anime.start(message)
         return True

    elif text == 'мой плейлист':
        await b_playlist.start(sql_user, message)
        return True

    # elif text == 'настройки':
    #     await b_settings.start(sql_user, message)
    #     return True

    elif text == 'закрыть меню':
        await message.answer("Меню закрыто", reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = False).ReplyKeyboardRemove())












