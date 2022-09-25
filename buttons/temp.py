from config import bot, logger, Sql_anime_playlist, session
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utilities.sql import get_user_by_telegram_id
from aiogram.utils.callback_data import CallbackData

cl_anime_subscribe = CallbackData('anime_subscribe', 'action', 'anime_id')


async def send_anime_post(sql_anime, message: Message):
    sql_user = await get_user_by_telegram_id(message.from_user.id)
    keyboard = await get_buttons(sql_anime, sql_user)


    text = f"{sql_anime.name}\nПросмотренно: ?\nВышло серий: {sql_anime.last_series} из {sql_anime.series}"  # TODO допилить
    try:
        if sql_anime.image[-4:] == 'webp':
            await bot.send_sticker(
                    message.from_user.id,
                    sql_anime.image,
                    disable_notification=True
            )
        else:
            await bot.send_photo(  # TODO допилить размер
                    message.from_user.id,
                    sql_anime.image,
                    disable_notification=True,
            )
        await bot.send_message(
                message.from_user.id,
                text,
                reply_markup=keyboard,
                disable_notification=True  # True - Бесшумный режим включен
        )
    except Exception:
        logger.error(f'Не удалось отправить ответ для {message.from_user.id}')

#
# async def get_buttons(sql_anime, sql_user):
#
#     sql_play_list = session.query(Sql_anime_playlist).filter_by(user_id= sql_user.id, anime_id= sql_anime.id).first()
#     if sql_play_list and sql_play_list.subscribe == True:
#         b_anime_status = InlineKeyboardButton(text='Отписаться от аниме', callback_data=cl_anime_subscribe.new(action='subscribe/unsubscribe',  anime_id=sql_anime.id))
#     else:
#         b_anime_status = InlineKeyboardButton(text='Подписаться на аниме', callback_data=cl_anime_subscribe.new(action='subscribe/unsubscribe',  anime_id=sql_anime.id))
#
#
#     keyboard = InlineKeyboardMarkup()
#     keyboard.add(InlineKeyboardButton(text='Смотреть', url=sql_anime.anime_urls[0].url))
#     keyboard.add(b_anime_status)
#     return keyboard
#
#



