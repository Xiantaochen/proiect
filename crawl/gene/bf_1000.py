import asyncio
from pyppeteer import launch
from .exe_js  import js1, js5, js3, js4
from lxml import etree
import re
import json
import os
from multiprocessing import Pool
import time

os.chdir('C:/Users/kobe/Desktop')

contents = []
urls = []
async def getHtmlContent(url=None,semaphore =None ):
    async with semaphore:
        print(url + " is crawling")
        browser = await launch(
            executablePath='F:/anzhuangbao/chrome-win/chrome.exe',
            timeout=15000,
            ignoreHTTPSErrors=True,
            devtools=False,
            headless=True
        )
        page = await browser.newPage()
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3819.0 Safari/537.36')

        # 设置页面视图大小
        await page.setViewport(viewport={'width': 1280, 'height': 800})

        # 是否启用JS，enabled设为False，则无渲染效果
        await page.setJavaScriptEnabled(enabled=False)
        await page.goto(url = url, timeout=0, waitUntil='networkidle2')
        await page.evaluate(js1)
        await page.evaluate(js3)
        await page.evaluate(js4)
        await page.evaluate(js5)
        await asyncio.sleep(2)
        content = await page.content()
        print(url + " is crawling")
        contents.append(content)
        urls.append(url)

def  parseContent(content = None, url = None):
    print(url  + " is crawled")
    gene_dict = {}
    Etree = etree.HTML(content)
    External_Ids_list = []
    alias = Etree.xpath('//*[@id="aliases_descriptions"]/div[1]/div[1]/div//h3')
    for i in range(len(alias)):
        source = Etree.xpath('//*[@id="aliases_descriptions"]/div[1]/div[1]/div[{}]//h3/text()'.format(i + 1))[0].strip()  # div索引从1开始，与Python不一样
        if str(source).startswith("External"):
            External_Ids = Etree.xpath(
                '//*[@id="aliases_descriptions"]/div[1]//div[{}]/div/ul//li//text()'.format(i + 1))
            href_list = Etree.xpath(
                '//*[@id="aliases_descriptions"]/div[1]//div[{}]/div/ul//li/a/@href'.format(i + 1))
            gene_name = url.rsplit("=", 1)[1]
            gene_dict['name'] = gene_name
            gene_dict['alias'] = None

            external_1 = [x.strip(": ") for x in External_Ids[0::2]]
            external_2 = External_Ids[1::2]

            for i in range(len(href_list)):
                External_Ids_list.append({'name': external_1[i], 'source': href_list[i], 'id': external_2[i]})
            break

    gene_dict['external'] = External_Ids_list

    Summaries_list = []
    result = Etree.xpath('//*[@id="summaries"]/div/div/h3/text()')
    for i in range(len(result)):
        title = Etree.xpath('//*[@id="summaries"]/div[{}]/div/h3/text()'.format(i + 1))[0].strip()
        content = Etree.xpath('//*[@id="summaries"]/div[{}]//p//text()'.format(i + 1)) # //text()得到的内容比较复杂，需要自己拼接
        if len(content) == 1:
            content = content[0].strip()
            Summaries_list.append({'name': title, 'description': content if content else None})
        else:
            content = [re.sub(r'\s+', ' ', x.replace("\r\n", " ").strip()) for x in content]
            content = " ".join(content[:-1]) + "."
            content.replace(" . ", ". ")

            if content == ".":
                content = None
            Summaries_list.append({'name': title, 'description': content if content else None})

    gene_dict['summary'] = Summaries_list

    position = Etree.xpath('//*[@id="genomic_location"]/div/div[3]/div/div')
    position_tmp = []
    for i in position:
        position_tmp = (i.xpath(".//*[@class='dl-inline']//text()"))
    position_list = [x for x in position_tmp if "\n" not in x]
    gene_dict['location'] = [{'pos': position_list[0], 'chr': position_list[0].split(":")[0],
                              'version': position_list[1].split("/")[1].strip(")"), 'size': position_list[3],
                              'orientation': position_list[5]},
                             {'pos': position_list[6], 'chr': position_list[6].split(":")[0],
                              'version': position_list[7].split("/")[1].strip(")"), 'size': position_list[9],
                              'orientation': position_list[11]}]

    with open('result_new2.json', 'a') as f:
        json.dump(gene_dict, f, indent=4)
        f.write(',\n')



def fetch_page(gene_list):
    base_url = 'https://www.genecards.org/cgi-bin/carddisp.pl?gene='
    fetch_list = []
    with open(gene_list) as f1:
        for line in f1:
            gene = line.strip().split(",")
            fetch_list.extend(gene)
    url_list = [base_url + x for x in fetch_list]
    return url_list

def main_get_html():
    sema = asyncio.Semaphore(4)
    url_list = fetch_page("du5.txt")
    tasks = [asyncio.ensure_future(getHtmlContent(url=url, semaphore=sema)) for url in url_list]
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

'''
多进程调用总函数，解析html
'''
def main_parse_html():
    p = Pool(6)
    i = 0
    for html, url in zip(contents, urls):
        i += 1
        p.apply_async(parseContent,args=(html, url))
    p.close()
    p.join()


if __name__ == '__main__':
    start = time.time()
    main_get_html()   # 调用方
    main_parse_html() # 解析html
    print('总耗时：%.5f秒' % float(time.time()-start))