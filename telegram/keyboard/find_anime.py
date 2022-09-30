from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import desc
from service.alchemy import session, Sql_anime
from telegram.keyboard import anime_posts
from telegram.loader import dp


async def start( message: Message ):
    button_menu = ReplyKeyboardMarkup(resize_keyboard = False)
    button_menu.add(InlineKeyboardButton("Найти аниме"))
    button_menu.add(InlineKeyboardButton('Показать 10 новых аниме'))

    await message.answer("Найти аниме:", reply_markup = button_menu)


@dp.message_handler(text=['Найти аниме'])
async def start(message: Message):
    await find_last_anime_in_bd(message, 10)


async def find_last_anime_in_bd(message: Message, count):
    last_ten_anime = session.query(Sql_anime).order_by(desc(Sql_anime.last_update)).limit(count).all()
    for sql_anime in last_ten_anime:
        await anime_posts.send_anime_post(sql_anime, message.from_user.id)



