# https://roscontrol.com/testlab/
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

url = 'https://roscontrol.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}


def errorHandle(elem):
    return None if elem is None else elem.text


def getProdCatalog(items):
    array = []
    # todo: add work with button "next"
    for item in items:
        data = {
            'name_of_product': item.find('div', attrs={'class': 'product__item-link'}).text,
            'general_rating': errorHandle(item.find('div', attrs={'class': 'rating-value'})),
            'reference': url + item['href']}

        ratingBlock = item.find('div', attrs={'class': 'rating-block'})
        if ratingBlock is None:
            continue

        rating_block = []
        rates = ratingBlock.findChildren('div', recursive=False)
        for rate in rates:
            if 'blacklist-desc' in rate['class'][0]:
                mark = {'rate': '0', 'name': 'Черный список'}
            else:
                mark = {'rate': rate.find('div', attrs={'class': 'right'}).text,
                        'name': rate.find('div', attrs={'class': 'text'}).text}
            rating_block.append(mark)

        data['params'] = rating_block
        array.append(data)

    return array


def getCatalog(catalogs, lastElementName):
    a, b = []
    for catalog in catalogs:
        if 'Птица' in catalog.text:
            return b

        if lastElementName == catalog.text or lastElementName in catalog.text:
            return data

        flag = False
        data = {'name': catalog.text.replace('\n', ''),'reference': url + catalog['href']}
        response = requests.get(url + catalog['href'], headers)
        soup = bs(response.text, 'html.parser')

        items = soup.find_all('a', attrs={'class': 'block-product-catalog__item'})
        if items:
            data['subCatalog'] = getProdCatalog(items)
            flag = True
            b.append(data)
            continue
        else:
            a.append(getCatalog(soup.find_all('a', attrs={'class': 'catalog__category-item'}), lastElementName))

        if not flag:
            data['subCatalog'] = a[0].copy()
            b.append(data)
            a.clear()

        if flag:
            return data
    return b


def getLastElement(items):
    for item in items:
        last = item
    return last


def main():
    response = requests.get(url + "/testlab", headers=headers)
    soup = bs(response.text, 'html.parser')

    items = soup.find_all('a', attrs={'class': 'catalog__category-item'})
    catalog = getCatalog(items, 'Бытовая техника') #getLastElement(items)

    return catalog

    #pprint(catalog)
