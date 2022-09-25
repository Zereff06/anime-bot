from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import bot, logger, Sql_anime_playlist, session

from utilities.sql import get_user_by_telegram_id
from aiogram.utils.callback_data import CallbackData


cl_anime_settings = CallbackData('settings','anime_id', 'action', 'value')


async def send_anime_post(sql_anime, telegram_ids):

    keyboard = await get_buttons(sql_anime)

    # text = f"{sql_anime.name}\nПросмотренно: ?\nВышло серий: {sql_anime.last_series} из {sql_anime.series}"  # TODO допилить
    text = f"{sql_anime.name}\nВышла новая серия: {sql_anime.last_series} из {sql_anime.series}"  # TODO допилить
    for telegram_id in telegram_ids:
        try:
            if sql_anime.image[-4:] == 'webp':
                await bot.send_sticker(
                        telegram_id,
                        sql_anime.image,
                        disable_notification=True
                )
            else:
                await bot.send_photo(  # TODO допилить размер
                        telegram_id,
                        sql_anime.image,
                        disable_notification=True,
                )
            await bot.send_message(
                    telegram_id,
                    text,
                    reply_markup=keyboard,
                    disable_notification=True  # True - Бесшумный режим включен
            )
        except Exception:
            logger.error(f'Не удалось отправить ответ для {telegram_id}')






async def get_buttons(sql_anime):

    b_settings = InlineKeyboardButton(text='...', callback_data=cl_anime_settings.new(anime_id =sql_anime.id, action = 'hidden_anime_settings', value='show' ))

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Смотреть', url=sql_anime.anime_urls[0].url))
    keyboard.add(b_settings)
    return keyboard

