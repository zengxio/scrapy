# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class Sp2Pipeline(object):
    def __init__(self):
        self.f=None

    def process_item(self, item, spider):
        """
        :param item: 爬虫中yield回来的对象
        :param spider: 爬虫对象，obj=JiandanSpider
        :return:
        """
        print(item)

        self.f.write("...") #写入。item是一个class对象
        return item

    @classmethod
    def from_crawler(cls, crawler):
        """
        初始化时候，用于创建pipeline对象
        :param crawler:可以去配置文件里面取值
        :return:
        """
        return cls() #直接实例化

    def open_spider(self, spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        print('000000')
        self.f=open('a.log','a+')


    def close_spider(self, spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        print('111111')
        self.f.close()


class Sp3Pipeline(object):
    def __init__(self):
        self.f=None

    def process_item(self, item, spider):
        """
        :param item: 爬虫中yield回来的对象
        :param spider: 爬虫对象，obj=JiandanSpider
        :return:
        """
        print(item)
        # if spider.anme=="jiandan":
        #     pass

        self.f.write("...") #写入。item是一个class对象
        #将item传递给下一个pipeline的process_item犯法
        # return item
        #下一个pipeline的process_item方法不再执行
        raise DropItem()

    @classmethod
    def from_crawler(cls, crawler):
        """
        初始化时候，用于创建pipeline对象
        :param crawler:可以去配置文件里面取值
        :return:
        """
        return cls() #直接实例化

    def open_spider(self, spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        print('000000')
        self.f=open('a.log','a+')


    def close_spider(self, spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        print('111111')
        self.f.close()