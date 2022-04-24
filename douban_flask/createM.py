# -*- coding = utf-8 -*-
# @Time: 2022/4/8 14:23
# @Author: mk310
# @File: createM.py
# @Software:PyCharm

import sqlite3
sql= '''
    create table message
    (
    title text,
    text text,
    user text,
    date text
    )
'''    #创建数据表
conn = sqlite3.connect('message2.db')
cur = conn.cursor()
datae = ['"efefef"','"fefefefdvvv"','"oooooo"','"ppppppp"']
sqlw = '''
               insert into message (title,text,user,date)
               values(%s)'''%",".join(datae)

print(sqlw)
# print(sql) #测试用 输出sql语句
cur.execute(sqlw)
conn.commit()

conn.close()
print('创建数据库完毕')
