import requests
from fake_useragent import UserAgent
from random import choice
import json
from config import logger, TEST_MODE
from Proxy_List_Scrapper import Scrapper


def check_amount_of_proxy():
    global proxy_list
    if len(proxy_list) < 50 and not TEST_MODE:
        proxy_list = get_proxy_list()


def get_header():
    user_agent = UserAgent()
    return {'headers': user_agent.random}


def get_html(url):
    if TEST_MODE:
        return read_file(url)

    check_amount_of_proxy()

    i = 0
    broken_proxy = []
    proxy = choice(proxy_list)

    html = requests.get(url, headers=get_header(), proxies=proxy).text
    while len(html) < 2 and i < 50:
        broken_proxy.append(proxy)

        proxy = choice(proxy_list)
        html = requests.get(url, headers=get_header(), proxies=proxy).text
        i += 1
        logger.error(f'#{i} Прокси не работает {proxy}')
    if i == 50:
        logger.error('Не удалось спарсить сайт {url}')
        return False

    for _proxy in broken_proxy:
        proxy_list.pop(_proxy)

    if TEST_MODE:
        write_file(html, url)

    return html


def write_file(text, name):
    name = _refact_name(name)
    with open(name, 'w', encoding='utf-8') as f:
        if isinstance(text, str):
            f.write(text)
        else:
            f.write(json.dumps(text, ensure_ascii=False))


def read_file(name, is_json=False):
    try:
        name = _refact_name(name)
        with open(name, encoding='utf-8') as f:
            if is_json:
                return json.load(f)
            else:
                return ''.join(f.readlines())
                # return f.readlines()
    except Exception:
        logger.error(f"Не удалось прчесть файл:  {name}")


def _refact_name(name: str):
    name = name.replace('https://', '')
    name = name.replace('.ru?a=', '-')
    for site_name, site_url in sites.items():
        if site_url in name:
            name = name.replace(site_url, "")
            name = site_name + name
    if name[-1] == "/":
        name = name[:-1]

    return 'data/' + name + '.html'


def get_proxy_list():
    if TEST_MODE:
        return [{'http://': 'http://74.205.128.200:80'}, {'http://': 'http://13.66.222.94:80'}]

    scrapper = Scrapper(category='US', print_err_trace=False)
    data = scrapper.getProxies()
    new_proxy_list = []
    for proxy in data.proxies:
        new_proxy_list.append({'http://': 'http://' + proxy.ip + ':' + proxy.port})
    logger.info(f'Loaded {len(new_proxy_list)} proxies')
    return new_proxy_list


proxy_list = get_proxy_list()

sites = {
    "anime_bit": "https://anime-bit.ru?a="
}
