from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardButton
# from config import session, Sql_anime, Sql_anime_urls
from buttons.find_anime import show_last_10_anime
# from buttons.find_anime.anime_bit_find_by_name import name_anime_bit_find_by_name

name_last_ten_anime = 'Показать 10 новых аниме'




async def show_button_menu( message: Message ):
    button_menu = ReplyKeyboardMarkup(resize_keyboard = False)
    # button_menu.add(InlineKeyboardButton("Найти аниме"))
    button_menu.add(InlineKeyboardButton(name_last_ten_anime))
    # button_menu.add(InlineKeyboardButton(name_find_by_name))
    # button_menu.add(InlineKeyboardButton("Настройки"))

    await message.answer("Найти аниме:", reply_markup = button_menu)


async def check(message: Message):
    text = message.text
    # if text == name_anime_bit_find_by_name:
    #     await anime_bit_find_by_name.start(message)
    #     return True


    if text == name_last_ten_anime:
        await show_last_10_anime.start(message)
        return True






async def start(message: Message):
    await show_button_menu(message)

