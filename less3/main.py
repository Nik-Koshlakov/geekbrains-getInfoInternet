import web_parser as wp
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


def addNewProductInDB(object):
    try:
        db.rosControl.insert_one(object)
    except dke:
        print('Document already exist')


def searchProducts(list, parentName):
    items = []

    if type(list) == type(dict()):
        if list['subCatalog'] is not None:
            parentName = list['name']
            list = list['subCatalog']

    if type(list) == type([]):
        for el in list:
            if el.get('name_of_product') is not None:
                el['parent_name'] = parentName
                items.append(el)
            else:
                items.append(searchProducts(el, parentName))

    return items


catalogs = wp.main()

client = MongoClient('localhost', 27017)
db = client['parserWebSites']
rosControl = db.rosControl
rosControl.create_index('name_of_product', unique=True)

test_object = {
    'name_of_product': 'Молоко "Экомилк" 3,2% пастеризованное',
    'params': [{'name': 'Безопасность', 'rate': 95},
               {'name': 'Натуральность', 'rate': 75},
               {'name': 'Пищевая ценность', 'rate': 67},
               {'name': 'Качество', 'rate': 79}],
    'reference': 'https://roscontrol.com/product/moloko-ekomilk/',
    'parent_name': 'Молоко',
    'general_rating': 60
}

addNewProductInDB(test_object)

products = searchProducts(catalogs, '')

# добавление в БД
for product in products:
    for podProduct in product:
        for el in podProduct:
            addNewProductInDB(el)

# поиск по рейтингу
r = int(input('Введите значение рейтинга для поиска товара по общему рейтингу или качеству: '))
find_result = db.rosControl.find({'$or': [{'params.3.rate': {'$gt': r}}, {'general_rating': {'$gt': r}}]})
wp.pprint(list(find_result))
