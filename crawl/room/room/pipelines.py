# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import pymysql
import elasticsearch_dsl
class MongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()

    def process_item(self, item, spider):
        self.client.room.lianjia.insert(item)
        return item

    def close_spider(self,spider):
        self.client.close()

class MysqlPipeline(object):
    def open_spider(self, spider):
        self.client = pymysql.connect(host = "localhost", port=3306, user ="root", password ="302811",
                                      charset = "utf8")
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        args = [item["total"],
                item["unitPrice"],
                item["xiaoQu"],
                item["quYu"],
                item["huYing"],
                item["louCeng"],
                item["zhuangXiu"],
                item["gongNuan"],
                item["chanQuan"],
                item["yongTu"],
                item["nianXian"],
                item["diYa"]
                ]
        sql = 'insert into t_lianjia VALUES (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(self, args)
        self.client.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.client.close()

class ElasticsearchPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()

    def process_item(self, item, spider):
        self.client.room.lianjia.insert(item)
        return item

    def close_spider(self,spider):
        self.client.close()

class CsvPipeline(object):

    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/spiders/articles.csv'
        print("***************************************************************")
        # 打开(创建)文件

        self.file = open(store_file, 'a+', encoding="utf-8",newline = '')
        # csv写法
        self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        print("正在写入......")
        if item['article_title']:
            # 主要是解决存入csv文件时出现的每一个字以‘，’隔离
            self.writer.writerow(
                [item['total'], item["unitPrice"], item["xiaoQu"], item["quYu"], item["huYing"],
                 item["louCeng"],item["zhuangXiu"], item["gongNuan"], item["chanQuan"],item["yongTu"],item["nianXian"],
                 item["diYa"]])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
