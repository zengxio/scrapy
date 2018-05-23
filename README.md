1.起始url -parse
	
class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['http://chouti.com/']
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,dont_filter=True,callback=self.parse1)
    
    def parse1(self, response):
        pass
		
2.POST请求，请求头，cookie
import urllib.parse
urllib.parse.urlencode({'k1':'v1','k2':'v2'}) 变成'k2=v2&k1=v1'
当'Content-Type': 'application/json'。数据格式如下
body={'k1':'v1','k2':'v2'}

示例:
	Request(
            url='http://dig.chouti.com/login',
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            body='phone=8615131255089&password=pppppppp&oneMonth=1',
			#body=urllib.parse.urlencode(post_dict),
			#body=urllib.parse.urlencode({'linksId': link_id}), #From data
            #cookies=self.cookie_dict,
            callback=self.check_login
        )

2.5 cookie
from scrapy.http.cookies import CookieJar

cookie_jar=CookieJar() 对象，封装了cookie
cookie_jar.extract_cookies(response,response.request)#去响应中获取cookie
cookie_dict={} #将cookie变成字典
#循环取出 cookie 并生成字典格式
for k, v in cookie_jar._cookies.items():
	for i, j in v.items():
		for m, n in j.items():
			self.cookie_dict[m] = n.value
			
3.持久化，items，pipeline
	pipeline执行的前提
		在spider中yield Item对象。使用item直接导入from ..items import Sp2Item  yield Sp2Item(url=url,text=text)
		在settings中注册
			ITEM_PIPELINES = {
			   'sp2.pipelines.Sp2Pipeline': 300,
			   'sp2.pipelines.Sp2Pipeline': 100, #越小越优先
			}
	编写pipeline

		class Sp2Pipeline(object):
		#     """
		#     检测该类是否有from_crawler方法。
		#         如果有
		#             obj=类.from_crawler()
		#         如果没有
		#             obj=类() #正常实例化
		#     obj.open_spider() #打开一个爬虫
		#     while True:
		#         爬虫运行，并且执行parse各种各样的方法,yield item
		#         obj.process_item() #只有这个方法循环执行
		#     obj.close_spider() #关闭一个爬虫
		#
		#     """
		
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
                #         val = crawler.settings.getint('MMMM') #配置文件MMM="xxx".直接get也行
                #         return cls(val)
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

	
	阻止第二个pipeline的process_item方法执行
	from scrapy.exceptions import DropItem
	def process_item(self, item, spider):
		if spider.name=="jiandan": #控制pipeline单独执行哪个爬虫
            pass

        #将item传递给下一个pipeline的process_item方法
        # return item
        #下一个pipeline的process_item方法不再执行
        raise DropItem()
	
	pipeline是全局生效，所有爬虫都会执行。可以通过spider.name指定只运行在哪个爬虫上
		
4.自定义去重规则
	类
	class RepeatUrl:
		def __init__(self):
			self.visited_url = set() #放在当前服务器的内存

		@classmethod
		def from_settings(cls, settings):
			"""
			初始化时，调用
			:param settings: 
			:return: 
			"""
			return cls()

		def request_seen(self, request):
			"""
			检测当前请求是否已经被访问过
			:param request: 
			:return: True表示已经访问过；False表示未访问过
			"""
			if request.url in self.visited_url:
				return True
			self.visited_url.add(request.url)
			return False

		def open(self):
			"""
			开始爬去请求时，调用
			:return: 
			"""
			print('open replication')

		def close(self, reason):
			"""
			结束爬虫爬取时，调用
			:param reason: 
			:return: 
			"""
			print('close replication')

		def log(self, request, spider):
			"""
			记录日志
			:param request: 
			:param spider: 
			:return: 
			"""
			print('repeat', request.url)
	配置文件中指定
	DUPEFILTER_CLASS = 'sp2.rep.RepeatUrl'
	
	默认是
	DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'
	DUPEFILTER_DEBUG = False
	JOBDIR = "保存范文记录的日志路径，如：/root/"  # 最终路径为 /root/requests.seen
			
5.中间件
	爬虫中间件
	内置爬虫中间件：
        'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': 50,
        'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': 500,
        'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': 700,
        'scrapy.contrib.spidermiddleware.urllength.UrlLengthMiddleware': 800,
        'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': 900,
		
	settings.py
	#SPIDER_MIDDLEWARES = {
	#    'sp3.middlewares.Sp3SpiderMiddleware': 543,
	#} #注册中间件
	#每个方法的返回值也不相同

	下载中间件
	默认下载中间件
    {
        'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
        'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
        'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
        'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
        'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
        'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': 580,
        'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,
        'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
        'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
        'scrapy.contrib.downloadermiddleware.chunked.ChunkedTransferMiddleware': 830,
        'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
        'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
    }
	
	#DOWNLOADER_MIDDLEWARES = {
	#    'sp3.middlewares.Sp3DownloaderMiddleware': 543,
	#}#注册中间件
	#process_request方法里面，使用:1、代理，下载需要增加代理请求头的。2、修改response返回值
	
6.自定义扩展
#基于信号自定义扩展
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
		
在settings里面注册信号
EXTENSIONS = {
   # 'scrapy.extensions.telnet.TelnetConsole': None,
   #路径，优先级
   'sp2.extends.MyExtension': 200,
}
7.其他
	配置文件
		# 1. 爬虫名称
		BOT_NAME = 'step8_king'

		# 2. 爬虫应用路径
		SPIDER_MODULES = ['step8_king.spiders']
		NEWSPIDER_MODULE = 'step8_king.spiders'

		# Crawl responsibly by identifying yourself (and your website) on the user-agent
		# 3. 客户端 user-agent请求头
		# USER_AGENT = 'step8_king (+http://www.yourdomain.com)'

		# Obey robots.txt rules
		# 4. 禁止爬虫配置
		# ROBOTSTXT_OBEY = False

		# Configure maximum concurrent requests performed by Scrapy (default: 16)
		# 5. 并发请求数
		# CONCURRENT_REQUESTS = 4

		# Configure a delay for requests for the same website (default: 0)
		# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
		# See also autothrottle settings and docs
		# 6. 延迟下载秒数
		# DOWNLOAD_DELAY = 2


		# The download delay setting will honor only one of:
		# 7. 单域名访问并发数，并且延迟下次秒数也应用在每个域名
		# CONCURRENT_REQUESTS_PER_DOMAIN = 2
		# 单IP访问并发数，如果有值则忽略：CONCURRENT_REQUESTS_PER_DOMAIN，并且延迟下次秒数也应用在每个IP
		# CONCURRENT_REQUESTS_PER_IP = 3

		# Disable cookies (enabled by default)
		# 8. 是否支持cookie，cookiejar进行操作cookie
		# COOKIES_ENABLED = True
		# COOKIES_DEBUG = True

		# Disable Telnet Console (enabled by default)
		# 9. Telnet用于查看当前爬虫的信息，操作爬虫等...
		#    使用telnet ip port ，然后通过命令操作est()查看爬虫的运行状况
		# TELNETCONSOLE_ENABLED = True
		# TELNETCONSOLE_HOST = '127.0.0.1'
		# TELNETCONSOLE_PORT = [6023,]


		# 10. 默认请求头
		# Override the default request headers:
		# DEFAULT_REQUEST_HEADERS = {
		#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		#     'Accept-Language': 'en',
		# }


		# Configure item pipelines
		# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
		# 11. 定义pipeline处理请求
		# ITEM_PIPELINES = {
		#    'step8_king.pipelines.JsonPipeline': 700,
		#    'step8_king.pipelines.FilePipeline': 500,
		# }



		# 12. 自定义扩展，基于信号进行调用
		# Enable or disable extensions
		# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
		# EXTENSIONS = {
		#     # 'step8_king.extensions.MyExtension': 500,
		# }


		# 13. 爬虫允许的最大深度，可以通过meta查看当前深度；0表示无深度
		# DEPTH_LIMIT = 3

		# 14. 爬取时，0表示深度优先Lifo(默认)；1表示广度优先FiFo

		# 后进先出，深度优先
		# DEPTH_PRIORITY = 0
		# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleLifoDiskQueue'
		# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.LifoMemoryQueue'
		# 先进先出，广度优先

		# DEPTH_PRIORITY = 1
		# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
		# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

		# 15. 调度器队列
		# SCHEDULER = 'scrapy.core.scheduler.Scheduler'
		# from scrapy.core.scheduler import Scheduler


		# 16. 访问URL去重
		# DUPEFILTER_CLASS = 'step8_king.duplication.RepeatUrl'
		
		"""
		17. 自动限速算法
			from scrapy.contrib.throttle import AutoThrottle #修改该类就可以自定以延迟时间
			自动限速设置
			1. 获取最小延迟 DOWNLOAD_DELAY
			2. 获取最大延迟 AUTOTHROTTLE_MAX_DELAY
			3. 设置初始下载延迟 AUTOTHROTTLE_START_DELAY
			4. 当请求下载完成后，获取其"连接"时间 latency，即：请求连接到接受到响应头之间的时间
			5. 用于计算的... AUTOTHROTTLE_TARGET_CONCURRENCY
			target_delay = latency / self.target_concurrency
			new_delay = (slot.delay + target_delay) / 2.0 # 表示上一次的延迟时间
			new_delay = max(target_delay, new_delay)
			new_delay = min(max(self.mindelay, new_delay), self.maxdelay)
			slot.delay = new_delay
		"""

		# 开始自动限速
		# AUTOTHROTTLE_ENABLED = True
		# The initial download delay
		# 初始下载延迟
		# AUTOTHROTTLE_START_DELAY = 5
		# The maximum download delay to be set in case of high latencies
		# 最大下载延迟
		# AUTOTHROTTLE_MAX_DELAY = 10
		# The average number of requests Scrapy should be sending in parallel to each remote server
		# 平均每秒并发数
		# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

		# Enable showing throttling stats for every response received:
		# 是否显示
		# AUTOTHROTTLE_DEBUG = True

		# Enable and configure HTTP caching (disabled by default)
		# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings


		"""
		18. 启用缓存
			目的用于将已经发送的请求或相应缓存下来，以便以后使用
			
			from scrapy.downloadermiddlewares.httpcache import HttpCacheMiddleware
			from scrapy.extensions.httpcache import DummyPolicy
			from scrapy.extensions.httpcache import FilesystemCacheStorage
		"""
		# 是否启用缓存策略
		# HTTPCACHE_ENABLED = True

		# 缓存策略：所有请求均缓存，下次在请求直接访问原来的缓存即可
		# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"
		# 缓存策略：根据Http响应头：Cache-Control、Last-Modified 等进行缓存的策略
		# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.RFC2616Policy"

		# 缓存超时时间
		# HTTPCACHE_EXPIRATION_SECS = 0

		# 缓存保存路径
		# HTTPCACHE_DIR = 'httpcache'

		# 缓存忽略的Http状态码
		# HTTPCACHE_IGNORE_HTTP_CODES = []

		# 缓存存储的插件
		# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



	代理
		代理，需要在环境变量中设置
		from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware#代理中间件
		
		方式一：使用默认
			os.environ
			{
				http_proxy:http://root:woshiniba@192.168.11.11:9999/
				https_proxy:http://192.168.11.11:9999/
			}
		方式二：使用自定义下载中间件
		
		def to_bytes(text, encoding=None, errors='strict'):
			if isinstance(text, bytes):
				return text
			if not isinstance(text, six.string_types):
				raise TypeError('to_bytes must receive a unicode, str or bytes '
								'object, got %s' % type(text).__name__)
			if encoding is None:
				encoding = 'utf-8'
			return text.encode(encoding, errors)
			
		class ProxyMiddleware(object):
			def process_request(self, request, spider):
				PROXIES = [
					{'ip_port': '111.11.228.75:80', 'user_pass': ''},
					{'ip_port': '120.198.243.22:80', 'user_pass': ''},
					{'ip_port': '111.8.60.9:8123', 'user_pass': ''},
					{'ip_port': '101.71.27.120:80', 'user_pass': ''},
					{'ip_port': '122.96.59.104:80', 'user_pass': ''},
					{'ip_port': '122.224.249.122:8088', 'user_pass': ''},
				]
				proxy = random.choice(PROXIES)
				if proxy['user_pass'] is not None:
					request.meta['proxy'] = to_bytes（"http://%s" % proxy['ip_port']）
					encoded_user_pass = base64.encodestring(to_bytes(proxy['user_pass']))
					request.headers['Proxy-Authorization'] = to_bytes('Basic ' + encoded_user_pass) #本质上就是设置了一个请求头
					print "**************ProxyMiddleware have pass************" + proxy['ip_port']
				else:
					print "**************ProxyMiddleware no pass************" + proxy['ip_port']
					request.meta['proxy'] = to_bytes("http://%s" % proxy['ip_port'])
		#注册代理中间件
		DOWNLOADER_MIDDLEWARES = {
		   'step8_king.middlewares.ProxyMiddleware': 500,
		}
		
	
	https证书
		Https访问时有两种情况：
		1. 要爬取网站使用的可信任证书(默认支持)
			DOWNLOADER_HTTPCLIENTFACTORY = "scrapy.core.downloader.webclient.ScrapyHTTPClientFactory"
			DOWNLOADER_CLIENTCONTEXTFACTORY = "scrapy.core.downloader.contextfactory.ScrapyClientContextFactory"
			
		2. 要爬取网站使用的自定义证书
			DOWNLOADER_HTTPCLIENTFACTORY = "scrapy.core.downloader.webclient.ScrapyHTTPClientFactory"
			DOWNLOADER_CLIENTCONTEXTFACTORY = "step8_king.https.MySSLFactory" #修改这个就行。配置文件里写
			
			# https.py
			from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory
			from twisted.internet.ssl import (optionsForClientTLS, CertificateOptions, PrivateCertificate)
			
			class MySSLFactory(ScrapyClientContextFactory):
				def getCertificateOptions(self):
					from OpenSSL import crypto
					v1 = crypto.load_privatekey(crypto.FILETYPE_PEM, open('/Users/wupeiqi/client.key.unsecure', mode='r').read())
					v2 = crypto.load_certificate(crypto.FILETYPE_PEM, open('/Users/wupeiqi/client.pem', mode='r').read())
					return CertificateOptions(
						privateKey=v1,  # pKey对象
						certificate=v2,  # X509对象
						verify=False,
						method=getattr(self, 'method', getattr(self, '_ssl_method', None))
					)
	
8.自定义命令
	让所有爬虫开始工作
		在爬虫同级目录创建任意目录，如commands
		在其创建命令为命名的文件crawlall.py
		内容如下
		from scrapy.commands import ScrapyCommand
		from scrapy.utils.project import get_project_settings


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
				spider_list = self.crawler_process.spiders.list()
				for name in spider_list:
					# print(name)
					#初始化爬虫
					self.crawler_process.crawl(name, **opts.__dict__)
				#开始执行所有的爬虫
				self.crawler_process.start()

		在settings.py下注册COMMANDS_MODULE ="sp3.commands"
		在项目目录执行命令：scrapy crawlall 