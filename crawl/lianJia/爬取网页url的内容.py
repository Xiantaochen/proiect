import requests
from lxml import etree
from urllib.request import urlretrieve
import os
from queue import Queue
from utils.common import getMd5

urlQueue = Queue()
urlSet = set()

def getUrlList():
    url = "https://su.lianjia.com/ershoufang/pg1/"

    headers = {
        "User-Agent" :"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
        "host":"su.lianjia.com"
    }

    sess = requests.session()
    sess.headers = headers
    resp = sess.get(url)

    Etree = etree.HTML(resp.content)

    image = Etree.xpath('//ul[@class = "sellListContent"]/li[1]/a/img[@class="lj-lazy"]/@data-original')[0]
    imageMd5 = getMd5(image)
    urlSet.add(imageMd5)
    title= Etree.xpath('//ul[@class = "sellListContent"]/li[1]/div/div[@class = "title"]//text()')[0]  #标题
    basePath = os.path.join(os.getcwd(), "image")
    filename = "images/{}.jpg".format(title)
    urlretrieve(image,filename=filename)
    datalurl = Etree.xpath('//ul[@class = "sellListContent"]/li[1]/div/div[@class = "title"]/a/@href')

    # address  = Etree.xpath('//ul[@class = "sellListContent"]/li[1]/div/div[@class = "address"]//text()')
    # flood = Etree.xpath('//ul[@class = "sellListContent"]/li[1]/div/div[@class = "flood"]//text()')
    # flowInfo = Etree.xpath('//ul[@class = "sellListContent"]/li[1]/div/div[@class = "followInfo"]//text()')
    # tag = Etree.xpath('//ul[@class = "sellListContent"]/li[1]/div/div[@class = "tag"]//text()')
    # totalPrice = Etree.xpath('//ul[@class = "sellListContent"]/li[1]/div/div[@class = "priceInfo"]/div[1]//text()')
    # unitPrice = Etree.xpath('//ul[@class = "sellListContent"]/li[1]/div/div[@class = "priceInfo"]/div[2]//text()')
    return image,datalurl

print(getUrlList())


