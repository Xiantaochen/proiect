"""
抓取豆瓣top260电影
库： aitohttp + asyncio
"""
import os
import asyncio
import aiohttp
from lxml import etree
from urllib.request import urlretrieve

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170'
}

async def getUrl(url,semaphore = None):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url = url, headers = headers) as resp:
                if resp.status == 200 :
                    html = await resp.text()
                    print(html)
                    print(resp.status)
                    Etree = etree.HTML(html)
                    urls  = Etree.xpath('//div[@class="hd"]/a/@href')
                    for url in urls:
                        await asyncio.sleep(2)
                        await getUrlResult(url = url)


async  def getUrlResult(url = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            html = await resp.text()
            Etree = etree.HTML(html)
            moveInfo ={}
            title = Etree.xpath('//span[@property="v:itemreviewed"]/text()')[0]
            year = Etree.xpath('//span[@class="year"]/text()')[0]
            year = str(year).replace("(","").replace(")","")
            director = Etree.xpath('//a[@rel="v:directedBy"]/text()')[0]
            rating = Etree.xpath('//strong[@class="ll rating_num"]/text()')[0]
            moveInfo["title"] = title
            moveInfo["year"] = year
            moveInfo["director"] =  director
            moveInfo['rating'] = rating
            print(moveInfo)




async def main():
    sema = asyncio.Semaphore(3)
    tasks = [asyncio.ensure_future(getUrl(url= url, semaphore=sema)) for url in ['https://movie.douban.com/top250?start={}&filter='.format(i*25) for i in range(0,10)]]
    await asyncio.wait(tasks)




asyncio.get_event_loop().run_until_complete(main())