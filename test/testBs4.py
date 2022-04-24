# -*- coding = utf-8 -*-
# @Time: 2022/3/6 16:26
# @Author: mk310
# @File: testBs4.py
# @Software:PyCharm
#beautiful 将html文档转换成一个复杂十五树形结构，每个节点都是python的对象，所有对象可以分为四种
'''
-tag
-NavigableString
-beautifulsoup
-Comment
'''
import re

from bs4 import BeautifulSoup

file = open("./baidu.html","rb")#只读方式打开文件
html = file.read()
bs = BeautifulSoup(html,"html.parser")#使用html解析器解析
'''

#tag 默认输出第一个标签及其属
print(bs.title)
print(bs.a)  #输出第一个为a的
print(type(bs.body))

#NavigableString 标签内容
print(bs.title.string)#标签里的内容
print(bs.a.attrs)#标签的属性

#Beautifulsoup 表示整个文档
print(bs.name)

#Comment 特殊的navi 去掉注释
print(bs.a.string)

'''
#应用

# 文档的遍历
#print(bs.head.contents) 更多内容搜索文档


# 文档的搜索
# 1
t_lsit = bs.find_all("a")#查找所有与字符串匹配的结果
print(t_lsit[1])

##参数
# t_lsit = bs.find_all(id = "suggResult")
# print(t_lsit)
# text参数
t_lsit = bs.find_all(re.compile("\d"))
print(t_lsit)
#limit参数
t_lsit = bs.find_all("a",limit=3)
print(t_lsit)


#2 正则表达式
# t_lsit = bs.find_all((re.compile("a")))
# print(t_lsit)

#3 方法 传入函数 根据方法搜索

#4 css选择器(标签 属性 类名 id )
list =  bs.select("title")
print(list)

