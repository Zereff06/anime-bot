from telegram.loader import dp, types
from service import parsing
from parsers import anime_bit
from telegram.keyboard import anime_posts

@dp.message_handler(lambda text: 'anime-bit.ru' in text.text)
async def parse_anime_bit_handler(message):
    url = message.text
    soup = parsing.get_soup(url)
    if soup is False:
        return await message.reply('Неверная ссылка!')

    sql_anime = await anime_bit.add_anime_to_db_from_anime_page(soup, url)
    await anime_posts.send_anime_post(sql_anime, message.from_user.id)