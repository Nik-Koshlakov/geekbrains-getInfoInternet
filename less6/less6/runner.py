<<<<<<< HEAD
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from less6 import settings
from less6.spiders.hhru import HhruSpider
from less6.spiders.superjob import SuperjobSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    #process.crawl(HhruSpider)
    process.crawl(SuperjobSpider)

=======
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from less6 import settings
from less6.spiders.hhru import HhruSpider
from less6.spiders.superjob import SuperjobSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    #process.crawl(HhruSpider)
    process.crawl(SuperjobSpider)

>>>>>>> 6bea1820ac6123d069c8044d870f945ba283ffbc
    process.start()