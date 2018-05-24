#!/usr/bin/env python
# -*- coding:utf-8 -*-
from twisted.internet import defer
from twisted.web.client import getPage
from twisted.internet import reactor
import threading


def _next_request():
    _next_request_from_scheduler()


def _next_request_from_scheduler():
    ret = getPage(bytes('http://www.chouti.com', encoding='utf8'))
    ret.addCallback(callback)
    ret.addCallback(lambda _: reactor.callLater(0, _next_request))


_closewait = None

@defer.inlineCallbacks
def engine_start():
    global _closewait
    _closewait = defer.Deferred()
    yield _closewait


@defer.inlineCallbacks
def task(url):
    reactor.callLater(0, _next_request)
    yield engine_start()


counter = 0
def callback(arg):
    global counter
    counter +=1
    if counter == 10:
        _closewait.callback(None)
    print('one', len(arg))


def stop(arg):
    print('all done', arg)
    reactor.stop()


if __name__ == '__main__':
    url = 'http://www.cnblogs.com'

    defer_list = []
    deferObj = task(url)
    defer_list.append(deferObj)

    v = defer.DeferredList(defer_list)
    v.addBoth(stop)
    reactor.run()

twisted示例三