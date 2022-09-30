import requests
from service import anonymity
from bs4 import BeautifulSoup as bs
import lxml



def get_soup(url):
    html = get_html(url)
    soup = bs(html, 'lxml')
    return soup

def get_html(url):
    random_proxy = anonymity.get_random_proxy()
    fake_user_agent = {'User-Agent': anonymity.get_fake_user_agent()}

    response = requests.get(url, headers=fake_user_agent, proxies=random_proxy)
    while True:
        if response.status_code == 200:
            return response.text
        elif len(anonymity.PROXY_LIST)< 5:
            anonymity.PROXY_LIST = anonymity.update_proxy_list()
        else:
            anonymity.PROXY_LIST.pop(anonymity.PROXY_LIST.index(random_proxy))