# https://roscontrol.com/testlab/
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

url = 'https://roscontrol.com'
# params = {'quick_filters': 'serials','tab': 'all','page': 1}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

prefix_catalog = ''

"""
catalog = {
    {
        "name": '',
        "url": '',
        "subcatalog": {
            "name": '',
            "url":'',
            "subcatalog": {
                "name": '',
                "url": '',
                "subcatalog": {
                    "name_product":'',
                    "params":{},
                    "general_rating":'',
                    "reference":''
                }
            }
        }
    }
}
"""


def errorHandle(elem):
    return None if elem is None else elem.text


response = requests.get(url + "/testlab", headers=headers)
soup = bs(response.text, 'html.parser')

# каталог товаров
catalog_products = soup.find_all('a', attrs={'class': 'catalog__category-item'})

for catalog_product in catalog_products:

    response1 = requests.get(url + catalog_product['href'], headers)
    soup1 = bs(response1.text, 'html.parser')

    catalog_items = soup1.find_all('a', attrs={'class': 'block-product-catalog__item'})
    if not catalog_items:
        # продукты
        catalog_items = soup1.find_all('a', attrs={'class': 'catalog__category-item'})  # href="/category/produkti/"
        for catalog_item in catalog_items:
            response2 = requests.get(url + catalog_item['href'], headers)
            soup2 = bs(response2.text, 'html.parser')

            podCatalog_items = soup2.find_all('a', attrs={'class': 'block-product-catalog__item'})
            if not podCatalog_items:
                # молочные, мясные....
                podCatalog_items = soup2.find_all('a', attrs={
                    'class': 'catalog__category-item'})  # href="/category/produkti/"
                for podCatalog_item in podCatalog_items:
                    # podCatalog_item.text.replace('\n', '').split(' ')[1]
                    response3 = requests.get(url + podCatalog_item['href'], headers)
                    soup3 = bs(response3.text, 'html.parser')

                    items = soup3.find_all('a', attrs={'class': 'block-product-catalog__item'})
                    if items:
                        # молоко
                        for info_item in items:
                            r_b = []
                            data = {
                                'name_of_product': info_item.find('div', attrs={'class': 'product__item-link'}).text,
                                'general_rating': errorHandle(info_item.find('div', attrs={'class': 'rating-value'})),
                                'reference': info_item['href'], 'params': r_b}
                            rating_block = info_item.find('div', attrs={'class': 'rating-block'})
                            if rating_block is None:
                                continue
                            rows = rating_block.findChildren('div', recursive=False)
                            for row in rows:
                                if 'blacklist-desc' in row['class'][0]:
                                    rating = {'rate': '0', 'name': 'Черный список'}
                                else:
                                    rating = {'rate': row.find('div', attrs={'class': 'right'}).text,
                                              'name': row.find('div', attrs={'class': 'text'}).text}
                                r_b.append(rating)

"""
while True:
    response = requests.get(url + '/popular/films/', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')

    serials_list = soup.find_all('div', attrs={'class': 'desktop-rating-selection-film-item'})
    if not serials_list or not response.ok:
        break
    # print(serials_list[0])
    serials = []

    for serial in serials_list:
        serial_data = {}
        serial_info = serial.find('p', attrs={'class': 'selection-film-item-meta__name'})

        serial_name = serial_info.text
        serial_link = url + serial_info.parent['href']

        serial_genre = serial.find('span', attrs={'class': 'selection-film-item-meta__meta-additional-item'}).next_sibling.text
        serial_rating = serial.find('span', attrs={'class': 'rating__value'}).text
        try:
            serial_rating = float(serial_rating)
        except:
            serial_rating = None

        serial_data['name'] = serial_name
        serial_data['link'] = serial_link
        serial_data['genre'] = serial_genre
        serial_data['rating'] = serial_rating

        serials.append(serial_data)
    params['page'] += 1

pprint(serials)
"""
