from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from service import sql
from telegram.loader import bot, dp
from telegram.handler import states
from telegram.keyboard import keyboards

anime_id_whose_questing = {}


@dp.message_handler(commands=['menu'])
async def start(message: types.Message):
    await keyboards.get_main_keyboard(message)


@dp.callback_query_handler(lambda c: "anime_post_watched_" in c.data)
async def anime_post_watched_(callback_query: types.CallbackQuery):
    anime_id = int(callback_query.data.split('_')[-1])
    watched_series = int(callback_query.message.text.split(' ')[-3])
    user_t_id = callback_query.from_user.id
    user_id = await sql.get_user_id_by_t_id(user_t_id)
    anime_state = await sql.set_playlist_series(user_id, anime_id, watched_series)

    if anime_state == 'added to db':
        await dp.current_state(user=user_t_id).set_state(states.Questions.how_many_series_user_watch)
        anime_id_whose_questing[user_id] = anime_id
        await bot.send_message(user_t_id, 'Аниме добавленно в плейлист!\nСколько вы просмотрели?')
    else:
        sql_anime = await sql.get_anime_by_id(anime_id)

        if anime_state == 'watching':
            await bot.send_message(user_t_id, f'{sql_anime.name}\nПросмотренно {watched_series} из {sql_anime.series}', disable_notification=True)

        elif anime_state == 'finished':
            await bot.send_message(user_t_id, f'{sql_anime.name}\nВсё просмотренно {watched_series} из {sql_anime.series}!', disable_notification=True)

    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(state=states.Questions.how_many_series_user_watch)
async def first_test_state_case_met(message: types.Message):
    text = message.text
    user_t_id = message.from_user.id
    user_id = await sql.get_user_id_by_t_id(user_t_id)

    if text.isnumeric():
        anime_id = anime_id_whose_questing[user_id]
        await sql.set_playlist_series(user_id, anime_id, int(text))

        del anime_id_whose_questing[user_id]
        await dp.current_state(user=user_t_id).reset_state()
        await message.reply('Обновлено :)')

    elif text.lower() == 'отмена':
        await dp.current_state(user=user_t_id).reset_state()
        del anime_id_whose_questing[user_id]
        await message.reply('Ну и ладна!', reply=False)
    else:
        await message.reply('Я тебя не понимаю :с\nЕсли не хотите отвечать, то напишете "Отмена"')


@dp.callback_query_handler(lambda c: "anime_post_subscribe_" in c.data)
async def anime_post_subscribe_(callback_query: types.CallbackQuery):
    user_t_id = callback_query.from_user.id
    user_id = await sql.get_user_id_by_t_id(user_t_id)
    anime_id = int(callback_query.data.split('_')[-1])
    sql_anime = await sql.get_anime_by_id(anime_id)

    status = await sql.subscribe_or_unsubscribe_to_anime(user_id, anime_id)
    if status == 'added to db':
        anime_id_whose_questing[user_id] = anime_id
        await dp.current_state(user=user_t_id).set_state(states.Questions.how_many_series_user_watch)
        await bot.send_message(user_t_id, 'Аниме добавленно в плейлист!\nСколько вы просмотрели?')
    elif status == 'watching':
        await bot.send_message(user_t_id, f'Вы подписались на {sql_anime.name}')
    elif status == 'drop':
        await bot.send_message(user_t_id, f'Вы отписались от {sql_anime.name}')

    await callback_query.message.edit_text(callback_query.message.text, reply_markup=await keyboards.get_post_settings(callback_query.message, anime_id))
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: "settings_" in c.data)
async def anime_post_settings_(callback_query: types.CallbackQuery):
    anime_id = int(callback_query.data.split('_')[-1])
    keyboard = await keyboards.get_post_settings(callback_query.message, anime_id)
    await  callback_query.message.edit_text(text=callback_query.message.text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: "anime_post_back_" in c.data)
async def anime_post_settings_(callback_query: types.CallbackQuery):
    anime_id = int(callback_query.data.split('_')[-1])
    sql_anime = await sql.get_anime_by_id(anime_id)
    keyboard = await keyboards.get_post_keyboard(sql_anime)

    await  callback_query.message.edit_text(text=callback_query.message.text, reply_markup=keyboard)



@dp.callback_query_handler(lambda c: "anime_post_set_series_" in c.data)
async def anime_post_set_series_(callback_query: types.CallbackQuery):
    user_t_id = callback_query.message.chat.id
    anime_id = int(callback_query.data.split('_')[-1])
    user_id = await sql.get_user_id_by_t_id(user_t_id)
    anime_id_whose_questing[user_id] = anime_id
    await dp.current_state(user=user_t_id).set_state(states.Questions.how_many_series_user_watch)
    await  callback_query.message.reply('Сколько вы просмотрели?', reply=False)
    await bot.answer_callback_query(callback_query.id)
