# from aiogram.types import Message
# from sites.anime_bit.parsing import Anime_bit_parser
# from sites.anime_bit.anime_bit import HOST_URL, POST_FIND
#
# from bot.send_posts import send_anime_post
# from sites.anime_bit.anime_bit import get_anime_or_add_to_bd_by_url
#
# name_anime_bit_find_by_name = 'Поиск по имени на anime-bit'
#
# async def check(message: Message, last_message):
#     if last_message == name_anime_bit_find_by_name:
#         await start(message)
#         return True
#     return False
#
#
# async  def start(message: Message):
#     anime_bit_parser = Anime_bit_parser(HOST_URL)
#     anime_data_array = await anime_bit_parser.get_title_info(HOST_URL + POST_FIND + message.text)
#
#     if not anime_data_array:
#         await message.answer("Не удалось найти данное аниме :с")
#         return
#
#     for anime in anime_data_array:
#         print(anime)