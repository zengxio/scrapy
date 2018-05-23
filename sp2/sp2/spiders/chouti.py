# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from scrapy.http import Request
from scrapy.http.cookies import CookieJar
from scrapy import Selector
class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['https://dig.chouti.com/']
    cookie_dict={}
    """
    1.发送一个GET请求，抽屉
        获取cookie
    2.用户名密码POST登录，携带上一次cookie
        返回值999
    3.携带cookie，点赞
    """

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,dont_filter=True,callback=self.parse)

    def parse(self, response):
        #response.text首页所有内容
        cookie_jar=CookieJar()
        cookie_jar.extract_cookies(response,response.request)

        #循环取出 cookie 并生成字典格式
        for k, v in cookie_jar._cookies.items():
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value

        post_dict={
            'phone':'8615915455813',
            'password':'zxywhx875199',
            'oneMonth':1,
        }

        #发送post请求进行登录
        yield Request(
            url='https://dig.chouti.com/login',
            method='POST',
            cookies=self.cookie_dict,
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            body=urllib.parse.urlencode(post_dict),

            callback=self.parse2 #执行成功在执行回调函数
        )

    def parse2(self,response):
        #获取新闻列表
        yield Request(url='https://dig.chouti.com',
                      method="GET",
                      cookies=self.cookie_dict,
                      callback=self.parse3)

    def parse3(self,response):
        #找div class=part2属性，去获取share-linkid
        hxs=Selector(response)
        link_id_list =hxs.xpath('//div[@class="part2"]/@share-linkid').extract()
        # for link_id in link_id_list:
        #     #http://dig.chouti.com/link/vote?linksId=19586021
        #     # 获取每个 id 去点赞
        #     base_url="https://dig.chouti.com/link/vote?linksId=%s"%(link_id)
        #     # 点赞(POST 的请求体可以不放数据)
        #     yield Request(url=base_url,
        #                   method="POST",
        #                   cookies=self.cookie_dict,
        #                   callback=self.parse4)

        #每一页都执行
        page_list=hxs.xpath('//div[@id="dig_lcpage"]//a/@href').extract()
        for page in page_list:
            #https://dig.chouti.com//all/host/recent/2#加前缀
            page_url="https://dig.chouti.com%s"%(page)
            yield Request(url=page_url,method='GET',callback=self.parse3)

        #取消点赞
        #https://dig.chouti.com/vote/cancel/vote.do
        page_url = "https://dig.chouti.com/vote/cancel/vote.do"
        for link_id in link_id_list:
            yield Request(url=page_url,
                          method='POST',
                          callback=self.parse4,
                          body=urllib.parse.urlencode({'linksId': link_id}), #From data
                          headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'},)


    def parse4(self,response):
        print(response.text)

