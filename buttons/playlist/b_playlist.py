from aiogram.types import Message
from config import session, Sql_anime, Sql_anime_playlist
from bot import send_posts

async def start(sql_user, message : Message):
    sql_anime_array = session.query(Sql_anime).join(Sql_anime_playlist).filter(Sql_anime_playlist.user_id == sql_user.id, Sql_anime_playlist.subscribe == True).all()
    for sql_anime in sql_anime_array:
        await send_posts.send_anime_post(sql_anime, [message.from_user.id])
