import requests
from lxml import etree
from urllib.request import urlretrieve
import os
from queue import Queue
from utils.common import getMd5

urlQueue = Queue()
urlSet = set()

def getUrlList():
    url = "https://su.lianjia.com/ershoufang/107101372222.html"

    headers = {
        "User-Agent" :"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
        "host":"su.lianjia.com",
        'Cookie':'TY_SESSION_ID=1b302b63-e91a-4cbd-b6f1-11156f8c92d7; lianjia_uuid=d2392ff9-a337-4019-97a0-90e5eeb1fe74; _smt_uid=5cfe432a.2ad57651; UM_distinctid=16b4136601149-0aa7591f52a597-3e38580a-1fa400-16b41366012352; _ga=GA1.2.611639012.1560167214; _jzqy=1.1560167211.1560783919.2.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6%E4%BA%8C%E6%89%8B%E6%88%BF; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b413663cf17a-05b35638764261-3e38580a-2073600-16b413663d0217%22%2C%22%24device_id%22%3A%2216b413663cf17a-05b35638764261-3e38580a-2073600-16b413663d0217%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22Main%22%2C%22%24latest_utm_content%22%3A%22Title%22%7D%7D; select_city=320500; all-lj=26155dc0ee17bc7dec4aa8e464d36efd; lianjia_ssid=9bc138b8-1914-4e2f-9e98-d784a5f964cd; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1560167212,1560181829,1560783924,1561204631; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1561204631; CNZZDATA1254525908=725069323-1560165699-https%253A%252F%252Fwww.baidu.com%252F%7C1561201404; CNZZDATA1254525948=57761940-1560165989-https%253A%252F%252Fwww.baidu.com%252F%7C1561201641; CNZZDATA1255633284=886035099-1560163506-https%253A%252F%252Fwww.baidu.com%252F%7C1561201131; CNZZDATA1255604082=464444706-1560163243-https%253A%252F%252Fwww.baidu.com%252F%7C1561201385; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiOGQxM2YzMzQ4MzFmOGE2NzgwYmIwMjFkMWJjODZhYTE2Mjg4NzYwOTIxZmM1ZmE5Zjc5NTIwZTRlMmNhNTYxNWVmOTJiYTQ5YjJjNzk4NDMxNzI5MWM1YmZhZWFmY2QzNTE5ODdiNDY3N2JmZDBlNzJlNjFmMzk0ODlkODFkZWE5NzI2NzVjYTljNjJiNzllMzg2ODhkZDIyNTMxM2MzMTBhYjA2M2FiYmM0NzYwMGZhMjVmODY2OWVmMThjOWJiMDNlY2RhODYxMWYwOTc2ZjAxMjYwYzFmZDlkZmVhM2I1MmM5MjBiMTZkZjE1ZmJmNDhjM2U1MTVmNDA2ODIyMGJlYjI5Y2Q4NTA2ZjI2MDljYjc4MGZiZmQ1ZThiMmRhMzdiNzg2NzMwNjZiMThlZDEzNDhmMmIxN2RlYWFhMDdcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiZTAyZjk2ZTNcIn0iLCJyIjoiaHR0cHM6Ly9zdS5saWFuamlhLmNvbS9lcnNob3VmYW5nLzEwNzEwMTM3MjIyMi5odG1sIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; _gid=GA1.2.1173950170.1561204662; _gat=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _qzja=1.713984965.1560167211061.1560865618349.1561204669455.1560865618349.1561204669455.0.0.0.21.7; _qzjc=1; _qzjto=1.1.0; _jzqa=1.2934735389460231000.1560167211.1560865618.1561204670.7; _jzqc=1; _jzqckmp=1; _qzjb=1.1561204669455.1.0.0.0; _jzqb=1.1.10.1561204670.1'
    }

    sess = requests.session()
    sess.headers = headers
    resp = sess.get(url)
    Etree  = etree.HTML(resp.content)
    price= Etree.xpath('//span[@class="total"]/text()')
    unitPrice = Etree.xpath('//span[@class="unitPriceValue"]//text()')
    roomSubInfo = Etree.xpath('//div[@class="room"]/div[2]/text()')
    typeMainInfo = Etree.xpath('//div[@class="type"]/div[1]/text()')
    typeSubInfo = Etree.xpath('//div[@class="type"]/div[2]/text()')
    AreaMainInfo = Etree.xpath('//div[@class="area"]/div[1]/text()')
    AreaSubInfo = Etree.xpath('//div[@class="area"]/div[2]/text()')
    label = Etree.xpath('//div[@class="base"]/div[2]//li[1]//text()')[1] #房屋户型
    label3 = Etree.xpath('//div[@class="base"]/div[2]//li[9]//text()')[1]  # 装修情况
    label4 = Etree.xpath('//div[@class="transaction"]/div[2]//li[1]//text()')[1] #挂牌时间
    label5 = Etree.xpath('//div[@class="houseRecord"]/span[2]/text()')[0] #链家编号

    print(price, unitPrice, roomSubInfo, typeMainInfo, typeSubInfo, AreaMainInfo, AreaSubInfo,
          label,  label3, label4, label5)

getUrlList()


