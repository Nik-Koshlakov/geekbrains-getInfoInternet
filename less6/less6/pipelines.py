# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from items import JobparserItem


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            result = self.process_salary_hh(item['salary'])
        elif spider.name == 'superjob':
            result = self.process_salary_superjob(item['salary'])

        item['salary_min'] = result['salary_min']
        item['salary_max'] = result['salary_max']
        item['currency'] = result['currency']
        del item['salary']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_superjob(self, salary):
        if not salary:
            salary_min = 0
            salary_max = 0
            currency = '-'

            return {'salary_min': salary_min, 'salary_max': salary_max, 'currency': currency}

        if 'от' in salary:
            salary_min = int(''.join(salary[2][:-4].split()))
            salary_max = 0
            currency = 'руб'
        elif 'до' in salary:
            salary_max = int(''.join(salary[2][:-4].split()))
            salary_min = 0
            currency = 'руб'
        else:
            salary_min = int(''.join(salary[0].split()))
            if ''.join(salary[1].split()) == '':
                salary_max = salary_min
            else:
                salary_max = int(''.join(salary[1].split()))
            currency = 'руб'

        return {'salary_min': salary_min, 'salary_max': salary_max, 'currency': currency}

    def process_salary_hh(self, salary):
        if 'з/п не указана' in salary:
            salary_min = 0
            salary_max = 0
            currency = '-'

        if 'USD' in salary:
            currency = 'usd'
        elif 'руб.' in salary:
            currency = 'руб'

        if 'до ' in salary:
            salary_min = 0
            salary_max = int(''.join(salary[1].split()))

        if 'от ' in salary:
            salary_min = int(''.join(salary[1].split()))
            if ' до ' in salary:
                salary_max = int(''.join(salary[3].split()))
            else:
                salary_max = 0

        return {'salary_min': salary_min, 'salary_max': salary_max, 'currency': currency}
