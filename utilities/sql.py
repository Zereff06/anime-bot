from config import session, Sql_anime, Sql_Users, Sql_anime_playlist, Sql_anime_urls, Sql_users_log
from loguru import logger
from aiogram.types import Message
from datetime import datetime

async def _check_nullable(result):
    if result is None:
        return False
    return result


async def get_user_by_telegram_id(telegram_id):
    result = session.query(Sql_Users).filter_by(telegram_id=telegram_id).first()
    return await _check_nullable(result)


async def get_user_id_by_telegram_id(telegram_id):
    result = session.query(Sql_Users.id).filter_by(telegram_id=telegram_id).first()[0]
    return await _check_nullable(result)


async def get_anime_by_anime_id(anime_id):
    result = session.query(Sql_anime).filter_by(id=anime_id).first()
    return await _check_nullable(result)


async def get_anime_playlist_by_user_id_and_anime_id(user_id, anime_id):
    result = session.query(Sql_anime_playlist).filter_by(user_id=user_id, anime_id=anime_id).first()
    return await _check_nullable(result)


async def subscribe_or_unsubscribe_to_anime(telegram_id, anime_id, new_status):
    sql_user = await get_user_by_telegram_id(telegram_id)

    sql_anime_playlist = session.query(Sql_anime_playlist).filter_by(anime_id=anime_id, user_id=sql_user.id).first()
    if sql_anime_playlist:
        sql_anime_playlist.subscribe = new_status
    else:
        new_anime_playlist = Sql_anime_playlist(
                user_id=sql_user.id,
                anime_id=anime_id,
                series=0,
                season=1,
                state='watching',
                subscribe=True
        )
        session.add(new_anime_playlist)
    session.commit()

    return True


async def add_anime_to_playlist(sql_user, sql_anime):
    new_anime_playlist = Sql_anime_playlist(
            user_id=sql_user.id,
            anime_id=sql_anime.id,
            series=1,
            season=sql_anime.season,
            state='watching',
            subscribe=True
    )
    session.add(new_anime_playlist)
    session.commit()


async def add_anime_to_bd(url, data):
    sql_new_anime = Sql_anime(
            name=data['name'],
            names=data['names'],
            season=data['season'],
            last_series=data['last_series'],
            series=data['series'],
            year=data['year'],
            genre=data['genre'],
            country=data['country'],
            description=data['description'],
            anime_type=data['anime_type'],
            image=data['image'],
            more_series=data['more_series']
    )

    session.add(sql_new_anime)
    session.commit()

    sql_anime = session.query(Sql_anime).filter_by(names=data['names']).first()
    sql_new_anime_urls = Sql_anime_urls(
            anime_id=sql_anime.id,
            url_type='site',
            site='anime_bit',
            url=url
    )
    session.add(sql_new_anime_urls)
    session.commit()

    logger.info(f"Аниме '{data['name']}' добавлено в базу")
    return sql_anime


async def get_anime_from_bd_by_name(anime_name):
    sql_anime = session.query(Sql_anime).filter(Sql_anime.names.like(f'%{anime_name}%')).first()
    if sql_anime is None:
        return False
    else:
        return sql_anime


async def get_user_and_add_log(message: Message):
    sql_user = await get_user_by_telegram_id(message.from_user.id)

    if not sql_user:
        sql_user = create_user(message)
    new_log = Sql_users_log(message.from_user.id, message.text)
    session.add(new_log)
    session.commit()
    return sql_user


async def create_user(message: Message):
    sql_user = session.query(Sql_Users).filter(Sql_Users.telegram_id == message.from_user.id).first()
    if sql_user:
        return
    else:
        new_user = Sql_Users(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language=message.from_user.language_code,
        )

        session.add(new_user)
        session.commit()
        return session.query(Sql_Users).filter_by(telegram_id=message.from_user.id).first()

async def update_anime_series(sql_anime, new_series):
    sql_anime.last_series = new_series
    sql_anime.last_update = datetime.now()
    session.commit()