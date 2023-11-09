import json
from statistics import mean
import msgpack


dataset = []

with open('./products_6_3.json', 'r', encoding='utf-8') as inp:
    dataset = json.load(inp)

name_dictionary = {}

for item in dataset:
    if item['name'] not in name_dictionary:
        name_dictionary[item['name']] = []

    name_dictionary.get(item['name']).append(item['price'])

def get_product_props(product_price_list: [int]):
    min_price = min(product_price_list)
    avg_price = mean(product_price_list)
    max_price = max(product_price_list)

    return min_price, avg_price, max_price

result_list = []

for product_name, values in name_dictionary.items():
    min_v, avg_v, max_v = get_product_props(values)
    result_list.append({
        'name': product_name,
        'min': min_v,
        'avg': avg_v,
        'max': max_v
    })

json_size = 0
with open('./products_6_3_res.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result_list))
    json_size = out.tell()

msgpk_size = 0
with open('./products_6_3_res.msgpack', 'wb') as out:
    out.write(msgpack.packb(result_list))
    msgpk_size = out.tell()

print(f"Size of JSON is {json_size}")
print(f"Size of MSGPACK is {msgpk_size}")
print(f"Size of JSON is larger than MSGPACK by {int(((json_size/msgpk_size) - 1)*100)}%")

