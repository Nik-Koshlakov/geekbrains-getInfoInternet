from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient


def getXPathDom(url, xpath_search):
    response = requests.get(url)
    dom = html.fromstring(response.text)

    return dom.xpath(xpath_search)


def getNewsXPathYandex():
    items = getXPathDom("https://yandex.ru/news/", "//article[contains(@class, 'mg-card')]")

    array_news = []
    for item in items:
        news = {}
        news['source'] = item.xpath(".//span[@class='mg-card-source__source']/a/@aria-label")[0]
        news['name'] = item.xpath(".//h2[@class='mg-card__title']/text()")[
            0]  # Ведомство ООН по правам человека поздравило Муратова и Рессе с Нобелевской премией мира
        news['ref'] = item.xpath(".//span[@class='mg-card-source__source']/a/@href")[0]
        # todo: change to uniform date format
        news['date'] = item.xpath(".//span[@class='mg-card-source__time']/text()")[0]  # 13:50

        array_news.append(news)

    return array_news


def getNewsXPathLenta():
    url_lenta = 'https://lenta.ru'
    items = getXPathDom(url_lenta, "//div[contains(@class,'item')]")

    array_news = []
    for item in items:
        name = item.xpath(".//a/text()")
        time1 = item.xpath("../..//span[contains(@class, 'g-date')]/text()")
        time2 = item.xpath(".//time[@class='g-time']/@datetime")

        if not name:
            continue
        if not time1 and not time2:
            continue

        news = {'source': 'Лента',
                'name': name[0],
                'ref': url_lenta + item.xpath(".//a/@href")[0],
                'date': time1[0] if time1 else time2[0]}

        array_news.append(news)

    return array_news


news = getNewsXPathYandex() + getNewsXPathLenta()

client = MongoClient('localhost', 27017)
db = client['parserWebSites']

if 'news' in db.list_collection_names():
    db['news'].drop()

news_db = db['news']
news_db.insert_many(news)

l = list(news_db.find())
pprint(l)
