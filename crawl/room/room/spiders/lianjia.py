# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://su.lianjia.com/ershoufang/pg{}/'.format(num) for num in range(1,10)]
    redis_key = "lianjia:start_urls"

    # index = 2
    # base_url = "https://bj.lianjia.com/ershoufang/pg{}/"
    # https://bj.lianjia.com/ershoufang/pg1
    def parse(self, response):
        urls  = response.xpath('//div[@class = "info clear"]/div[@class="title"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_info)
            pass
        # if self.index < 1000 :
        #     yield scrapy.Request(self.base_url.format(self.index), callback=self.parse)
        # self.index += 1

    def parse_info(self,response):
        total = response.xpath('concat(//span[@class = "total"]/text(),//span[@class = "unit"]/span/text())').extract_first()#总价
        unitPrice = response.xpath('string(//span[@class="unitPriceValue"])').extract_first() #单元价格
        xiaoQu = response.xpath('//a[@class = "info "]/text()').extract_first() #小区名称
        quYu  = response.xpath('string(//div[@class="areaName"]/span[@class = "info"])').extract_first() #所在区域
        base = response.xpath('//div[@class="base"]//ul')
        huYing = base.xpath('./li[1]/text()').extract_first() #户型
        louCeng = base.xpath('./li[2]/text()').extract_first() #楼层
        zhuangXiu = base.xpath('./li[9]/text()').extract_first() #装修
        gongNuan = base.xpath('./li[last()-1]/text()').extract_first() #供暖
        chanQuan = base.xpath('./li[last()]/text()').extract_first() #产权

        transaction = response.xpath('//div[@class="transaction"]')
        yongTu = transaction.xpath('.//li[4]/span[2]/text()').extract_first() #用途
        nianXian = transaction.xpath('.//li[5]/span[2]/text()').extract_first() #年限
        diYa = transaction.xpath('.//li[7]/span[2]/text()').extract_first().strip() #抵押
        pass

        yield {
            "total" : total,
            "unitPrice" : unitPrice,
            "xiaoQu" : xiaoQu,
            "quYu" : quYu,
            "huYing" : huYing,
            "louCeng" : louCeng,
            "zhuangXiu" : zhuangXiu,
            "gongNuan" : gongNuan,
            "chanQuan" : chanQuan,
            "yongTu" : yongTu,
            "nianXian" : nianXian,
            "diYa" : diYa
        }