from bs4 import BeautifulSoup
import json
import numpy

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

    site = BeautifulSoup(text, 'html.parser')
    products = site.find_all('div', attrs={"class": "product-item"})

    items = list()

    for product in products:
        item = dict()

        item['id'] = product.a['data-id']
        item['link'] = product.find_all('a')[1]['href']
        item['img_link'] = product.find_all('img')[0]['src']
        item['product_name'] = product.find_all('span')[0].get_text().strip()
        item['price'] = int(product.price.get_text().replace('₽', '').replace(' ', '').strip())
        item['bonus'] = int(product.strong.get_text().replace('+ начислим ', '').replace('бонусов', '').strip())

        properties = product.find_all('li')
        for prop in properties:
            item[prop['type']] = prop.get_text().strip()

        items.append(item)

    return items


items_list = list()

for i in range(1, 54):
    file_name_base = f'./t2/{i}.html'
    result = handle_file(file_name_base)
    items_list += result

items_list = sorted(items_list, key=lambda x: x['price'], reverse=True)

with open('./2_1_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items_list))

filter_items = list(filter(lambda x: x['bonus'] > 2436, items_list))

with open('./2_2_result.json', 'w', encoding="utf-8") as file:
    file.write(json.dumps(filter_items))


def process_statistics():
    result = dict()
    np_items = []

    for item in items_list:
        np_items.append(item['price'])
    np_items = numpy.asarray(np_items)

    result['sum'] = numpy.sum(np_items)
    result['avr'] = result['sum'] / np_items.shape[0]
    result['max'] = np_items.max()
    result['min'] = np_items.min()

    print(result)
    return result


def tag_processing():
    city_list = []
    city_dict = dict()

    for item in items_list:
        city_list.append(item['product_name'].lower())

    for city in city_list:
        if city in city_dict:
            city_dict[city] += 1
        else:
            city_dict[city] = 1

    res = dict(sorted(city_dict.items(), key=lambda x: x[1], reverse=True))

    return res


process_statistics()
tag_processing()
