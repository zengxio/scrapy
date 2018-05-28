#!/usr/bin/env python
#encoding:utf-8
#生成唯一标识
from scrapy.utils import request
from scrapy.http import Request
obj=Request(url="http://www.baidu.com?id=1&username='hah'")
# obj2=Request(url="http://www.baidu.com?username='hah'&id=1")
obj2=Request(url="http://www.baidu.comfdsafwefcx")
v=request.request_fingerprint(obj)
print(v)
v=request.request_fingerprint(obj2)
print(v)