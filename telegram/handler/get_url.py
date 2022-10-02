from telegram.loader import dp, types
from service import parsing, sql
from parsers import anime_bit
from telegram import anime_posts

@dp.message_handler(lambda text: 'anime-bit.ru' in text.text)
async def parse_anime_bit_handler(message: types.Message):

    url = message.text
    sql_anime = await sql.get_anime_by_url(url)
    if sql_anime is not None:
        await anime_posts.send_anime_post(sql_anime, message.from_user.id)
    else:
        soup = parsing.get_soup(url)
        if soup is False:
            return await message.reply('Неверная ссылка!')

        sql_anime = await anime_bit.add_anime_to_db_from_anime_page(soup, url)
        await anime_posts.send_anime_post(sql_anime, message.from_user.id)