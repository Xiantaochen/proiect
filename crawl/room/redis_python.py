# import redis
# import json
# import pymongo
#
# redis_client  = redis.Redis(host="localhost", port= 6379, db=0)
#
# while True:
#     key, value = redis_client.blpop("lianjia:items")
#     print(key)
#     print(json.loads(value))
#     d = json.loads(value)

# {'total': '315万',
#  'unitPrice': '27877元/平米',
#  'xiaoQu': '湖滨花园(吴中区)',
#  'quYu': '吴中\xa0郭巷\xa0内环至中环',
#  'huYing': '3室2厅1厨1卫',
#  'louCeng': '中楼层 (共18层)',
#  'zhuangXiu': '精装',
#  'gongNuan': '有',
#  'chanQuan': '70年',
#  'yongTu': '普通住宅',
#  'nianXian': '暂无数据',
#  'diYa': '无抵押'}


import csv
import time

import redis
import json

headers = ['总价', '单元价格','小区名称', '所在区域', '户型', '楼层','装修情况','配备电梯','产权年限','房屋用途','房屋年限','抵押信息']

redis_client  = redis.Redis(host="localhost", port= 6379, db=0)








while True:
    key, value = redis_client.blpop("lianjia:items")
    d = json.loads(value)
    print(d)
    rows = [d['total'], d['unitPrice'], d['xiaoQu'], d['quYu'].replace('\xa0', ' '),
            d['huYing'], d['louCeng'], d['zhuangXiu'], d['gongNuan'], d['chanQuan'],
            d['yongTu'], d['nianXian'], d['diYa']]

    with open('lianjia.csv', 'a') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(rows)

