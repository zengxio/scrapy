from scrapy import signals

class MyExtension(object):
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_crawler(cls, crawler):
        val = crawler.settings.getint('MMMM')
        ext = cls(val) #创建对象

        #在scrapy中注册信号spider_opened。第一个参数是触发信号时执行的函数
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened) #开始爬虫的时候执行
        # 在scrapy中注册信号spider_closed
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed) #结束爬虫的时候执行

        return ext

    def spider_opened(self, spider):
        print('open')

    def spider_closed(self, spider):
        print('close')