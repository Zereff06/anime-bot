import re
from service import sql, parsing
from telegram import anime_posts
from service.logger import logger

URL = 'https://anime-bit.ru'


async def start():
    soup = parsing.get_soup(URL)
    soup_posts = soup.find_all('div', {'class': 'anime_list'})

    for post in soup_posts:
        _name = post.find('a', {'class': 'link_title_list'})['title']
        post_name = re.sub('».*', '', _name.replace('«', ''))

        sql_anime = await sql.get_anime_by_name(post_name)

        if not sql_anime:
            sql_anime = await add_anime_to_db_from_home_page(post)
        try:
            new_series = int(post.find('div', {'class': 'anime_list_bottom_info'}).find_all('div')[1].text.replace(' Серии: [', '').replace(']', '').split(' из ')[0])
        except:
            logger.error(f'{_name} Ошибка при парсенге новый серии!')
            continue

        if sql_anime.last_series < new_series:
            await anime_posts.find_users_and_send_post_to_tg(new_series, sql_anime)
            await sql.update_anime_series(sql_anime, new_series)


async def add_anime_to_db_from_home_page(post):
    _name = post.find('a', {'class': 'link_title_list'})['title']
    post_name = re.sub('».*', '', _name.replace('«', ''))
    post_url = post.find('a', {'class': 'link_title_list'})['href']
    post_img = URL + post.find('a', {'class': 'anime_list_center_img'}).find('img')['src']

    _series = post.find('div', {'class': 'anime_list_bottom_info'}).find_all('div')[1].text.replace(' Серии: [', '').replace(']', '').split(' из ')
    post_current_series = _series[0]
    post_max_series = _series[1]
    more_series = '+' in _series[1]
    season = re.sub('.*?» .*?-', '', _name)

    year = post.find('div', {'class': 'anime_list_center_discription'}).find('div').text.replace('Год: ', '')
    genre = post.find('div', {'class': 'anime_list_center_discription'}).find_all('div')[1].text.replace('Жанр: ', '')
    country = post.find('div', {'class': 'anime_list_center_discription'}).find_all('div')[3].text.replace('Страна: ', '')
    description = post.find('div', {'class': 'anime_list_center_discription'}).find_all('div')[6].text.replace('Описание: ', '')

    anime_type = 'ТВ'
    if 'Фильм' in _name:
        anime_type = 'Фильм'

    return await sql.add_new_anime(name=post_name,
                                   season=season,
                                   series=post_max_series,
                                   last_series=post_current_series,
                                   year=year,
                                   genre=genre,
                                   country=country,
                                   description=description,
                                   anime_type=anime_type,
                                   image=post_img,
                                   more_series=more_series,
                                   url=post_url
                                   )


async def add_anime_to_db_from_anime_page(soup, url):
    _name = soup.find('div', {'class': 'anime_page_title'}).text.strip()
    post_name = re.sub('».*', '', _name.replace('«', ''))
    post_url = url
    post_img = URL + soup.find('div', {'class': 'img_box'}).find('img')['src']

    _series = soup.find('div', {'class': 'anime_page_upload'}).text
    post_current_series, post_max_series = re.sub('.*?\[', '', _series).replace(']', '').split(' из ')
    more_series = '+' in _series
    season = re.sub('.*?» .*?-', '', _name)

    year = soup.find('div', {'class': 'discription'}).find_all('div')[1].text.replace('Год: ', '')
    genre = soup.find('div', {'class': 'discription'}).find_all('div')[2].text.replace('Жанр: ', '')
    country = soup.find('div', {'class': 'discription'}).find_all('div')[4].text.replace('Страна: ', '')
    description = soup.find('div', {'class': 'discription'}).find('div', {'itemprop': 'description'}).text

    anime_type = 'ТВ'
    if 'Фильм' in _name:
        anime_type = 'Фильм'

    return await sql.add_new_anime(name=post_name,
                                   season=season,
                                   series=post_max_series,
                                   last_series=post_current_series,
                                   year=year,
                                   genre=genre,
                                   country=country,
                                   description=description,
                                   anime_type=anime_type,
                                   image=post_img,
                                   more_series=more_series,
                                   url=post_url
                                   )
