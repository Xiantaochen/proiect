# -*- coding: utf-8 -*-
import scrapy
import json
import re

class A66lawSpider(scrapy.Spider):
    name = '66law'
    allowed_domains = ['66law.cn']
    start_urls = ['https://www.66law.cn/lawyeronline/jtsg/page_{}.aspx'.format(num) for num in range(1,200)]

    def parse(self, response):
        i = 1
        while True:
                base = response.xpath('//div[@class="dlbox"]/dl[{}]'.format(i))
                lawyerInfo = {}
                xingMing = base.xpath('.//a/text()').extract_first() #姓名
                if xingMing != None :
                    quYu = base.xpath('.//span[@class="c999 lawyerarea"]/text()').extract_first() #区域
                    quYu = str(quYu).replace("[","").replace("]","")
                    shanChang = base.xpath('.//p[@class="other"][1]/text()').extract_first() #擅长
                    jiGou = base.xpath('.//p[@class="other"][2]/text()').extract_first() #机构
                    diZhi = base.xpath('.//p[@class="other"][3]/text()').extract_first() #地址
                    dianHua  = base.xpath('//b[@class="tel2"]/text()').extract_first() #电话号码
                    dianHua = str(dianHua).replace(" ","")
                    haoPing = base.xpath('./dd[1]/p[6]/text()[1]').extract_first()
                    AXJF = base.xpath('./dd[1]/p[6]/text()[2]').extract_first()
                    ZXBZRS = base.xpath('./dd[1]/p[6]/text()[3]').extract_first()
                    lawyerInfo['xingming'] = xingMing
                    lawyerInfo['quYu'] = quYu
                    lawyerInfo['shanChang'] = shanChang
                    lawyerInfo['jigou'] = jiGou
                    lawyerInfo['diZhi'] = diZhi
                    lawyerInfo['dianHua'] = dianHua
                    lawyerInfo['haoPing'] = haoPing
                    lawyerInfo['AXJF'] = AXJF
                    lawyerInfo['ZXBZRS'] = ZXBZRS
                    i += 1
                    print(lawyerInfo)
                else:
                    break



