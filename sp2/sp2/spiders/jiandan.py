# -*- coding: utf-8 -*-
import scrapy
from ..items import Sp2Item
from scrapy.http import Request
from scrapy import Selector
class JiandanSpider(scrapy.Spider):
    name = 'jiandan'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          dont_filter=True,
                          headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'},
                          callback=self.parse
                          )

    def parse(self, response):

        hxs=Selector(response)
        a_list=hxs.xpath('//div[@class="indexs"]/h2')
        for tag in a_list:
            text=tag.xpath('./a/text()').extract_first()
            url=tag.xpath('./a/@href').extract_first()
            yield Sp2Item(url=url,text=text) #引用pipeline

        #获取页码[url,url],每一页都执行

