import scrapy
from scrapy.http import HtmlResponse
from less6.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[contains(@class, 'f-test-vacancy-item')]/div/div/div/div/div/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//div[contains(@class ,'f-test-vacancy-base-info')]/div/div/div/div/h1/text()").get()
        salary = response.xpath("//div[contains(@class ,'f-test-vacancy-base-info')]/div/div/div/div/span/span/span/text()").getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item