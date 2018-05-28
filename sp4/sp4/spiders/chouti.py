# -*- coding: utf-8 -*-
import scrapy


class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['dig.chouti.com']
    start_urls = ['http://dig.chouti.com/']

    def parse(self, response):
        print(response)

#这个redisspider爬虫停不下来。
from scrapy_redis.spiders import RedisSpider
# class ChoutiSpider(RedisSpider):
#     name = 'chouti'
#     allowed_domains = ['dig.chouti.com']
#     """
#     REDIS_START_URLS_AS_SET = False 等于True去集合取值，否则去列表取值
#     """
#     #起始url REDIS_START_URLS_KEY = '%(name)s:start_urls'
#     def parse(self, response):
#         print(response)
#
