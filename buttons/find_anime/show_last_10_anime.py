from config import session, Sql_anime
from sqlalchemy import desc
from aiogram.types import Message
from bot.send_posts import send_anime_post


async def start(message: Message):
    last_ten_anime = session.query(Sql_anime).order_by(desc(Sql_anime.last_update)).limit(10).all()
    for sql_anime in last_ten_anime:
        await send_anime_post(sql_anime, [message.from_user.id])


async def check(message:Message):
    if message.text == "Показать 10 новых аниме":
        await start(message)
