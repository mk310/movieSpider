# -*- coding = utf-8 -*-
# @Time: 2022/3/2 21:03
# @Author: mk310
# @File: test.py
# @Software:PyCharm
import urllib.request
#获取get请求

# re = urllib.request.urlopen("http://www.baidu.com") #发出请求收到回应
# print(re.read().decode('utf-8')) #对获取的网页解码

# import urllib.parse
# #获取post请求 httpbin.org(测试网站)
# data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8") #带头发出请求 收到post，模拟真实请求
# re = urllib.request.urlopen("http://httpbin.org/post",data=data)
# print(re.read().decode('utf-8')) #对获取的网页解码

#掩饰爬虫
headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36 Edg/98.0.1108.62"}
url = "http://douban.com"
req = urllib.request.Request(url=url)
print(req)
