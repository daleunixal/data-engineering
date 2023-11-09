import json
import requests
from json2html import *

data = requests.get('http://dog-api.kinduff.com/api/facts').json()


test = json2html.convert(json=data)

print(test)

with open('r_html_task_6.html', 'w', newline='', encoding='utf-8') as result:
    result.write(test)