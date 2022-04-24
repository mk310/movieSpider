# -*- coding = utf-8 -*-
# @Time: 2022/3/11 16:16
# @Author: mk310
# @File: testSqlite.py
# @Software:PyCharm


import sqlite3
#1 创建数据库
conn = sqlite3.connect("test.db")   #打开或创建数据库文件

print("成功打开数据库")
c = conn.cursor()   #获取游标
#2 创建数据表


    # sql = '''
    #     create table company
    #             (id int primary key not null,
    #             name text not null,
    #             age int not null,
    #             address char(50),
    #             salary real)
    # '''
    # c.execute(sql)  #执行sql语句
    # conn.commit()   #提交数据库操作
    # conn.close()    #关闭
    #
    # print("成功建表")

#3 查询数据
# sql1 = '''
#       insert into company (id,name,age,address,salary)
#       values (1,"zhangsan",32,"chengdu",8000);
#
#    '''
# sql2 = '''
#       insert into company (id,name,age,address,salary)
#       values (2,"lisi",44,"chengdu",18000);
#
#    '''
# c.execute(sql1)
# c.execute(sql2) # 执行sql语句
#
#
# conn.commit()  # 提交数据库操作
# conn.close()  # 关闭
#
# print("成功建表")
# print("插入数据")

sql3 = " select id,name,address,salary from company "
cursor = c.execute(sql3)
for row in cursor:
    print("id = ",row[0])
    print("name = ", row[1])
    print("adress = ", row[2])
    print("salary ", row[3])

conn.close()
print('查询完成')