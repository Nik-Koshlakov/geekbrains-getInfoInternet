import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader
from scrapy.utils.deprecate import method_is_overridden
from scrapy import Spider
import warnings
from scrapy.http import Request


class AvitoSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    headers = {
        'User-Agent': 'MMozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/catalogue/dekor-dlya-mebeli/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads, headers=self.headers)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', "//h1[@slot='title']/text()")
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('photo', "//img[contains(@alt, 'image')]/@src")
        loader.add_xpath('character_name', "//div[@class='def-list__term']/text()")
        loader.add_xpath('character_value', "//div[@class='def-list__definition']/text()")
        return loader.load_item()
