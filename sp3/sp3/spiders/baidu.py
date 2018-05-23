# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com/']


    def parse(self, response):
        print(response.text)
