# crawl里面主要是4个项目
+ 第一个  Bilibili 的滑块验证
+ 第二个  pyppeteer + asyncio 
+ 第三个  app抓取抖音粉丝id
+ 第四个  scrapy_redis 抓取链家二手房
+ 第五个  asyncio + aiohttp抓取豆瓣电影信息

# app主要是用flask 做 restful后端接口开发 目前还在重构中....

# frontVue是用来用vue.js构建前端  未完成....

# jsEncrty 主要是更新网站js加密
+ 1.js 是http://hgwsbs.hg12333.com/hgwt/member/login.jhtml 的密码加密的js代码改写

# lianjia scrapy_redis集成了布隆过滤器的代码改写

### 布隆布隆过滤器代码, bloomfilter.py 并将此文件放置在scrapy_redis包下面
### pip安装mmh3无法安装时，可改为国内豆瓣源 pip install mmh3 -i https://pypi.douban.com/simple/

```python
# -*- coding: utf-8 -*-
import mmh3
import redis
import math
import time


class PyBloomFilter():
    #内置100个随机种子
    SEEDS = [543, 460, 171, 876, 796, 607, 650, 81, 837, 545, 591, 946, 846, 521, 913, 636, 878, 735, 414, 372,
             344, 324, 223, 180, 327, 891, 798, 933, 493, 293, 836, 10, 6, 544, 924, 849, 438, 41, 862, 648, 338,
             465, 562, 693, 979, 52, 763, 103, 387, 374, 349, 94, 384, 680, 574, 480, 307, 580, 71, 535, 300, 53,
             481, 519, 644, 219, 686, 236, 424, 326, 244, 212, 909, 202, 951, 56, 812, 901, 926, 250, 507, 739, 371,
             63, 584, 154, 7, 284, 617, 332, 472, 140, 605, 262, 355, 526, 647, 923, 199, 518]

    #capacity是预先估计要去重的数量
    #error_rate表示错误率
    #conn表示redis的连接客户端
    #key表示在redis中的键的名字前缀
    def __init__(self, capacity=1000000000, error_rate=0.00000001, conn=None, key='BloomFilter'):
        self.m = math.ceil(capacity*math.log2(math.e)*math.log2(1/error_rate))      #需要的总bit位数
        self.k = math.ceil(math.log1p(2)*self.m/capacity)                           #需要最少的hash次数
        self.mem = math.ceil(self.m/8/1024/1024)                                    #需要的多少M内存
        self.blocknum = math.ceil(self.mem/512)                                     #需要多少个512M的内存块,value的第一个字符必须是ascii码，所有最多有256个内存块
        self.seeds = self.SEEDS[0:self.k]
        self.key = key
        self.N = 2**31-1
        self.redis = conn
        # print(self.mem)
        # print(self.k)

    def add(self, value):
        name = self.key + "_" + str(ord(value[0])%self.blocknum)
        hashs = self.get_hashs(value)
        for hash in hashs:
            self.redis.setbit(name, hash, 1)

    def is_exist(self, value):
        name = self.key + "_" + str(ord(value[0])%self.blocknum)
        hashs = self.get_hashs(value)
        exist = True
        for hash in hashs:
            exist = exist & self.redis.getbit(name, hash)
        return exist

    def get_hashs(self, value):
        hashs = list()
        for seed in self.seeds:
            hash = mmh3.hash(value, seed)
            if hash >= 0:
                hashs.append(hash)
            else:
                hashs.append(self.N - hash)
        return hashs


pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=3)
conn = redis.StrictRedis(connection_pool=pool)

if __name__ == "__main__":
    bf = PyBloomFilter(conn=conn)
    bf.add('www.lianjia.com')
    print(bf.is_exist('www.lianjia.com'))

```

###修改scrapy_redis包下的 dupefilter.py 文件，改为

```python
import logging
import time

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from . import defaults
from .connection import get_redis_from_settings
from .bloomfilter import conn,PyBloomFilter   #导入布隆过滤器

logger = logging.getLogger(__name__)


# TODO: Rename class to RedisDupeFilter.
class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplicates filter.

    This class can also be used with default Scrapy's scheduler.

    """

    logger = logger

    def __init__(self, server, key, debug=False):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.

        """
        self.server = server
        self.key = key
        self.debug = debug
        self.logdupes = True

        # 集成布隆过滤器
        self.bf = PyBloomFilter(conn=conn, key=key)     # 利用连接池连接Redis

    @classmethod
    def from_settings(cls, settings):
        """Returns an instance from given settings.

        This uses by default the key ``dupefilter:<timestamp>``. When using the
        ``scrapy_redis.scheduler.Scheduler`` class, this method is not used as
        it needs to pass the spider name in the key.

        Parameters
        ----------
        settings : scrapy.settings.Settings

        Returns
        -------
        RFPDupeFilter
            A RFPDupeFilter instance.


        """
        server = get_redis_from_settings(settings)
        # XXX: This creates one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        # TODO: Use SCRAPY_JOB env as default and fallback to timestamp.
        key = defaults.DUPEFILTER_KEY % {'timestamp': int(time.time())}
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(server, key=key, debug=debug)

    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        fp = self.request_fingerprint(request)

        # 集成布隆过滤器
        if self.bf.is_exist(fp):    # 判断如果域名在Redis里存在
            return True
        else:
            self.bf.add(fp)         # 如果不存在，将域名添加到Redis
            return False

        # This returns the number of values added, zero if already exists.
        # added = self.server.sadd(self.key, fp)
        # return added == 0

    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        self.clear()

    def clear(self):
        """Clears fingerprints data."""
        self.server.delete(self.key)

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False
```
