from bs4 import BeautifulSoup
import re
import json
import numpy


def process_data(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')

        item = dict()

        item['city'] = site.find_all("span", string=re.compile('Город:'))[0].get_text().split(":")[1].strip()
        item['structure'] = site.find_all('h1')[0].get_text().split(":")[1].strip()
        address = site.find_all('p', attrs={'class': 'address-p'})[0].get_text()
        address = ''.join(re.split('Улица:', address))
        address = re.split('Индекс:', address)

        item['street'] = address[0].strip()
        item['index'] = address[1].strip()
        item['floors'] = int(site.find_all('span', attrs={'class': 'floors'})[0].get_text().split(':')[1].strip())
        item['year'] = int(
            site.find_all('span', attrs={'class': 'year'})[0].get_text().replace('Построено в', '').strip())
        item['parking'] = True if site.find_all("span", string=re.compile('Парковка:'))[0].get_text().split(":")[
                                      1].strip() == 'есть' else False
        item['img_url'] = site.find_all('img')[0]['src']
        item['rating'] = float(site.find_all("span", string=re.compile('Рейтинг:'))[0].get_text().split(":")[1].strip())
        item['views'] = int(site.find_all("span", string=re.compile('Просмотры:'))[0].get_text().split(":")[1].strip())

        return item


items = list()

for i in range(1, 1000):
    file_name_for_parsing = f"./t1/{i}.html"
    result = process_data(file_name_for_parsing)
    items.append(result)

items = sorted(items, key=lambda x: x['rating'], reverse=True)

with open('./1_1_result.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(items))

filtered_list = list(filter(lambda x: x['rating'] > 2, items))

with open('./1_2_result.json', 'w', encoding="utf-8") as file:
    file.write(json.dumps(filtered_list))


def process_stats():
    result_statistical = dict()
    np_items = []

    for item in items:
        np_items.append(item['views'])
    np_items = numpy.asarray(np_items)

    result_statistical['sum'] = numpy.sum(np_items)
    result_statistical['avr'] = result_statistical['sum'] / np_items.shape[0]
    result_statistical['max'] = np_items.max()
    result_statistical['min'] = np_items.min()

    return result_statistical


def process_frequ():
    cities = []
    count_city = dict()

    for item in items:
        cities.append(item['city'].lower())

    for city in cities:
        if city in count_city:
            count_city[city] += 1
        else:
            count_city[city] = 1

    result_tag = dict(sorted(count_city.items(), key=lambda x: x[1], reverse=True))

    return result_tag


process_stats()
process_frequ()
