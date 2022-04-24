from flask import Flask,render_template
import sqlite3
from flask import request,redirect,url_for
import time
import random
import string




conn = sqlite3.connect("movie2.db")
cur = conn.cursor()
# sql3 = "drop table userData"
# cur.execute(sql3)
# sql1 = '''create table kkk
# (
#     id        text,
#     data     text
# );'''

# data = cur.execute(sql1)


sql4 = "insert into kkk (id) values (1)"
cur.execute(sql4)


# for i in data:
#     print(i)

cur.close()
conn.close()
