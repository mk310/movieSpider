# -*- coding = utf-8 -*-
# @Time: 2022/5/13 17:00
# @Author: mk310
# @File: test.py
# @Software:PyCharm
from flask import Flask,render_template
import sqlite3
from flask import request,redirect,url_for
import time
import random
import string




conn = sqlite3.connect("movie.db")
cur = conn.cursor()
# sql3 = "drop table userData"
# cur.execute(sql3)

# 创建
# sql1 = '''create table userlog
# (
#     user       text,
#     password     text,
#     date     text
# );'''
#
# data = cur.execute(sql1)

# # 插入
# sql4 = "insert into userlog (user,password,date) values ('tom',111,'2022-04-23 17:20:34')"
# cur.execute(sql4)
# conn.commit()

# username = 'tom'
# sqluser = "select password,date from userlog where user = '%s'" % (username)
# userpasses = cur.execute(sqluser)
# for userpass in userpasses:
#     password = userpass[0]
#     date = userpass[1]
logusers = []
conn = sqlite3.connect("movie.db")
cur = conn.cursor()
sqlall = "select * from userlog "
allusers = cur.execute(sqlall)
for uer in allusers:
    user = []
    user.append(uer[0])
    user.append(uer[1])
    user.append(uer[2])
    logusers.append(user)
print(logusers)
users= []
sqlall = "DELETE FROM userlog WHERE date = '2022-05-13 19:26:13'"


allusers = cur.execute(sqlall)
conn.commit()

cur.close()
conn.close()
