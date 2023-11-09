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

channelViewCount_list = []
elapsedtime_list = []
videoCategoryId_list = []
videoCount_list = []
videoViewCount_list = []
videoLikeCount_list = []
videoDislikeCount_list = []
channelelapsedtime_list = []

dataset = []

with open('./ytb.json', 'r', encoding='utf-8') as inp:
    dataset = json.load(inp)

for item in dataset:
    channelViewCount_list.append(item['channelViewCount'])
    elapsedtime_list.append(item['elapsedtime'])
    videoCategoryId_list.append(item['videoCategoryId'])
    videoCount_list.append(item['videoCount'])
    videoViewCount_list.append(item['videoViewCount'])
    videoLikeCount_list.append(item['videoLikeCount'])
    videoDislikeCount_list.append(item['videoDislikeCount'])
    channelelapsedtime_list.append(item['channelelapsedtime'])

channelViewCount_list = list(filter(lambda x: x is not None, channelViewCount_list))
elapsedtime_list = list(filter(lambda x: x is not None, elapsedtime_list))
videoCategoryId_list = list(filter(lambda x: x is not None, videoCategoryId_list))
videoCount_list = list(filter(lambda x: x is not None, videoCount_list))
videoViewCount_list = list(filter(lambda x: x is not None, videoViewCount_list))
videoLikeCount_list = list(filter(lambda x: x is not None, videoLikeCount_list))
videoDislikeCount_list = list(filter(lambda x: x is not None, videoDislikeCount_list))
channelelapsedtime_list = list(filter(lambda x: x is not None, channelelapsedtime_list))

channelViewCount_list = list(map(lambda x: float(x), channelViewCount_list))
elapsedtime_list = list(map(lambda x: float(x), elapsedtime_list))
videoCategoryId_list = list(map(lambda x: float(x), videoCategoryId_list))
videoCount_list = list(map(lambda x: float(x), videoCount_list))
videoViewCount_list = list(map(lambda x: float(x), videoViewCount_list))
videoLikeCount_list = list(map(lambda x: float(x), videoLikeCount_list))
videoDislikeCount_list = list(map(lambda x: float(x), videoDislikeCount_list))
channelelapsedtime_list = list(map(lambda x: float(x), channelelapsedtime_list))

result = []

result.append({
    'channelViewCount': {
        'avg': mean(channelViewCount_list),
        'min': min(channelViewCount_list),
        'max': max(channelViewCount_list),
        'sum': sum(channelViewCount_list),
        'std_err': stats.sem(channelViewCount_list)
    },
    'elapsedtime': {
        'avg': mean(elapsedtime_list),
        'min': min(elapsedtime_list),
        'max': max(elapsedtime_list),
        'sum': sum(elapsedtime_list),
        'std_err': stats.sem(elapsedtime_list)
    },
    'videoCategoryId': {
        'avg': mean(videoCategoryId_list),
        'min': min(videoCategoryId_list),
        'max': max(videoCategoryId_list),
        'sum': sum(videoCategoryId_list),
        'std_err': stats.sem(videoCategoryId_list)
    },
    'videoCount': {
        'avg': mean(videoCount_list),
        'min': min(videoCount_list),
        'max': max(videoCount_list),
        'sum': sum(videoCount_list),
        'std_err': stats.sem(videoCount_list)
    },
    'videoViewCount': {
        'avg': mean(videoViewCount_list),
        'min': min(videoViewCount_list),
        'max': max(videoViewCount_list),
        'sum': sum(videoViewCount_list),
        'std_err': stats.sem(videoViewCount_list)
    },
    'videoLikeCount': {
        'avg': mean(videoLikeCount_list),
        'min': min(videoLikeCount_list),
        'max': max(videoLikeCount_list),
        'sum': sum(videoLikeCount_list),
        'std_err': stats.sem(videoLikeCount_list)
    },
    'videoDislikeCount': {
        'avg': mean(videoDislikeCount_list),
        'min': min(videoDislikeCount_list),
        'max': max(videoDislikeCount_list),
        'sum': sum(videoDislikeCount_list),
        'std_err': stats.sem(videoDislikeCount_list)
    },
    'channelelapsedtime': {
        'avg': mean(channelelapsedtime_list),
        'min': min(channelelapsedtime_list),
        'max': max(channelelapsedtime_list),
        'sum': sum(channelelapsedtime_list),
        'std_err': stats.sem(channelelapsedtime_list)
    },
})

with open('./task5_r.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result))

with open('./task5_r.msgpack', 'wb') as out:
    out.write(msgpack.packb(result))

df = pd.DataFrame([x for x in result])

with open('./task5_r.csv', 'w', encoding='utf-8') as out:
    out.write(df.to_csv(index=False))

df.to_pickle('./task5_r.pkl')

