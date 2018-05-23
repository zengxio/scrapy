from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
import os

class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        #分析源码
        """
            from scrapy.crawler import CrawlerProcess
            from scrapy.core.engine import ExecutionEngine
        """
        #爬虫列表
        from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
        os.environ['http_proxy']='http://root:woshiniba@192.168.11.11:9999/'
        os.environ['https_proxy']='http://192.168.11.11:9999/'
        spider_list = self.crawler_process.spiders.list()
        for name in spider_list:
            # print(name)
            #初始化爬虫
            self.crawler_process.crawl(name, **opts.__dict__)
        #开始执行所有的爬虫
        self.crawler_process.start()

