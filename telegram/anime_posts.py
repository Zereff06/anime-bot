from service import sql
from telegram.loader import bot
from service import images, logger
from telegram.keyboard import keyboards
from aiogram.utils.exceptions import WrongFileIdentifier



async def find_users_and_send_post_to_tg(new_series, sql_anime):

    sql_users = await sql.get_users_by_anime_in_playlist(new_series, sql_anime.id)

    for sql_user in sql_users:
        sql_playlist = sql.get_anime_playlists(sql_user.id, sql_anime.id)
        await send_anime_post(sql_anime, sql_user.telegram_id, sql_playlist)


async def send_anime_post(sql_anime: sql.Sql_anime, telegram_id, sql_playlist: sql.Sql_anime_playlist= None):

    if isinstance(sql_anime, int):
        sql_anime = await sql.get_anime_by_id(sql_anime)

    if sql_anime.t_image_id is None:
        exist_t_image_id = False
    else:
        exist_t_image_id = True

    keyboard = await keyboards.get_post_keyboard(sql_anime)

    if sql_playlist:
        text = f"{sql_anime.name}:\nПросмотрено: {sql_playlist.series}  из {sql_anime.last_series} (Всего {sql_anime.series})"
    else:
        text = f"{sql_anime.name}:\nВышло: {sql_anime.last_series} из {sql_anime.series}"

    try:
        if not exist_t_image_id:
           await _send_img_and_save_id(sql_anime, telegram_id)
        else:
            await _send_img(sql_anime, telegram_id)
    except WrongFileIdentifier:
        await _send_img_and_save_id(sql_anime, telegram_id)
    except Exception:
        logger.logger.error(f'Не удалось отправить ответ для {telegram_id} -> anime id: #{sql_anime.id} -> {text}')
    finally:
        await bot.send_message(
                telegram_id,
                text,
                reply_markup=keyboard,
                disable_notification=True
        )

async def _send_img(sql_anime, telegram_id):
    if sql_anime.image[-4:] == 'webp':
        await bot.send_sticker(
                telegram_id,
                sql_anime.t_image_id,
                disable_notification=True,
        )
    else:
        await bot.send_photo(
                telegram_id,
                sql_anime.t_image_id,
                disable_notification=True,
        )

async def _send_img_and_save_id(sql_anime, telegram_id):
    if sql_anime.image[-4:] == 'webp':
        msg = await bot.send_sticker(
                telegram_id,
                sql_anime.image,
                disable_notification=True,
        )

        await sql.add_t_image_id(sql_anime.id, msg.sticker.file_id)
    else:
        bio_image = images.change_image_size(sql_anime.image)
        msg = await bot.send_photo(
                telegram_id,
                bio_image,
                disable_notification=True,
        )
        await sql.add_t_image_id(sql_anime.id, msg.photo.file_id)