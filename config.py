from src import secret
from alchemy import *
from aiogram import Bot, Dispatcher
from loguru import logger

TEST_MODE = True

logger.add("logs/log.json",
           format="{time} {level} {message}",
           level="DEBUG",
           rotation="512 KB",
           compression="zip",
           serialize=True
           )

settings = {
    'API_TOKEN': secret.API_TOKEN,
    'ADMIN_ID': secret.ADMIN_ID,
    'HOST': 'https://www.okidoki.ee',
    'HOST_POSTS': 'https://www.okidoki.ee/ru/buy/',
    'EMOJI_ON' : "✅ ",
    'EMOJI_OFF' : "❌ ",

}

sort = {
    'best_is_top': 'fsort=1',
    'new_is_first': 'fsort=2',
    'old_is_top': 'fsort=3',
    'cheaper_is_top': 'fsort=4',
    'expensive_is_top': 'fsort=5'
}

buttons_dict = {
    'main_menu': {
        'key': '/menu',
        'name': { 'ru': 'Главное меню', 'eng': 'Main menu' }
    },
    'subscribe': {
        'name': { 'ru': 'Подписка/Отписка', 'eng': 'Subscribe/Unsubscribe' },
        'items': {
            'subscribe': { 'ru': 'Подписаться', 'eng': 'Subscribe' },
            'unsubscribe': { 'ru': 'Отписаться', 'eng': 'Unsubscribe' }
        }
    },
    'cities': {
        'name': { 'ru': 'Выбор города' },
        'key': { 'ru': 'Город' },
        'items': {
            'tallinn': { 'ru': 'Таллинн', 'cid': 'cid=1' },
            'tartu': { 'ru': 'Тарту', 'cid': 'cid=684' },
            'narva': { 'ru': 'Нарва', 'cid': 'cid=252' },
            'kohtla_jarve': { 'ru': 'Кохтла-Ярве', 'cid': 'cid=256' },
            'parnu': { 'ru': 'Пярну', 'cid': 'cid=532' },
            'johvi': { 'ru': 'Йыхви', 'cid': 'cid=261' },
            'maardu': { 'ru': 'Маарду', 'cid': 'cid=11' },
            'haapsalu': { 'ru': 'Хапсалу', 'cid': 'cid=386' },
            'rakvere': { 'ru': 'Раквере', 'cid': 'cid=423' },
            'viljandi': { 'ru': 'Вильянди', 'cid': 'cid=815' }
        }
    },
    'categories': {
        'name': { 'ru': 'Выбор категории' },
        'items':{
            "fashion_style_and_beauty" : "ru/buy/30/",
            "children`s_products" : "ru/buy/19/",
            "transport" : "ru/buy/16/",
            "home_and_usa" : "ru/buy/20/",
            "electronics" : "ru/buy/26/",
            "entertainment_and_hobby" : "ru/buy/23/",
            "sports_equipment" : "ru/buy/31/",
            "animals" : "ru/buy/3611/",
            "all_for_business" : "ru/buy/17/",
            "services" : "ru/buy/35/",
            "the_property" : "ru/buy/15/",
            "job" : "ru/buy/3612/"
        }
    }
}

# Bot
bot = Bot(token = settings['API_TOKEN'])
dp = Dispatcher(bot)

# SQL
session = Session()
