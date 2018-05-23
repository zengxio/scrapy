#!/usr/bin/env python
#encoding:utf-8
import subprocess
data={
    'www.inter-joy.cn':['122.115.36.177'],
    'www.inter-joy.com':['110.172.221.136'],
    'www.inter-joy.com.cn':['110.172.221.136'],
    'www.cailewu.com':['121.31.57.139','113.12.112.6'],
    'www.cailewu.net':['121.31.57.140','113.12.112.138'],
    'www.innosky.com.cn':['101.200.145.152'],
    'www.hibingo.com.cn':['123.207.114.114'],
    'www.haibingo.com':['123.207.111.235'],
      }

for k in data.items():
    cmd="ping %s"%(k[0])
    flag=False
    count=5
    while not flag and count<=5:
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = str(res.stdout.read() + res.stderr.read(), encoding='gbk')
        if result.strip():
            try:
                ip_addr=result.strip().split(']')[0].split('[')[1]
                if ip_addr in k[1]:
                    print(k[0],ip_addr,'is ok')
                else:
                    print(k[0],k[1],ip_addr,'is no')
            except IndexError as e:
                #'域名出现异常'
                print(k[0],result)
                break

            count=0
            flag=True
        else:
            count+=1
            continue

