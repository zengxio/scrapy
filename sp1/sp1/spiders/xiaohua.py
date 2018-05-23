# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.http import Request
class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['xiaohuar.com']
    start_urls = ['http://588ku.com/sucai/']

    def parse(self, response):
        hxs=Selector(response=response)
        user_list=hxs.xpath('//div[@class="clearfix Ind-recom-box"]')
        for i in user_list:
           result=i.xpath('div[@class="fl recom-list"]//a/@href')
           # print(result)
           yield Request(url=result,callback=self.parse)




