import json
from statistics import mean
from scipy import stats
import msgpack
import pandas as pd

# Работаем с полями
# channelViewCount: float
# elapsedtime: float
# videoCategoryId: float
# videoCount: float
# videoViewCount: float
# videoLikeCount: float
# videoDislikeCount: float
# channelelapsedtime: float

lookup_list = ['channelViewCount',
               'elapsedtime',
               'videoCategoryId',
               'videoCount',
               'videoViewCount',
               'videoLikeCount',
               'videoDislikeCount',
               'channelelapsedtime',
               ]

data_dict = {}

dataset = []

with open('./ytb.json', 'r', encoding='utf-8') as inp:
    dataset = json.load(inp)

for item in dataset:
    for key in item.keys():
        if key not in lookup_list:
            continue
        if key not in data_dict:
            data_dict[key] = []
        data_dict[key].append(item[key])


def process_metric_by_artifact(data_list: [], metric_name: str):
    filtered_list = list(filter(lambda x: x is not None, data_list))
    mapped_list = list(map(lambda x: float(x), filtered_list))

    return {
        metric_name: {
            'avg': mean(mapped_list),
            'min': min(mapped_list),
            'max': max(mapped_list),
            'sum': sum(mapped_list),
            'std_err': stats.sem(mapped_list)
        }
    }


result = list(map(lambda x: process_metric_by_artifact(data_dict[x], x), list(data_dict.keys())))

with open('./task5_r.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result))

with open('./task5_r.msgpack', 'wb') as out:
    out.write(msgpack.packb(dataset))

df = pd.DataFrame([x for x in dataset])

with open('./task5_r.csv', 'w', encoding='utf-8') as out:
    out.write(df.to_csv(index=False))

df.to_pickle('./task5_r.pkl')
