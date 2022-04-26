from flask import Flask,render_template
import sqlite3
from flask import request,redirect,url_for
import time
import random
import string
import functools

#数据库中提取用户信息
users = []
conn = sqlite3.connect("movie.db")
cur = conn.cursor()
sql = "select * from userData"
data = cur.execute(sql)
conn.commit()
for item in data:
    user = []
    user.append(item[0])
    temp = item[1]
    temp = temp.split('|')
    mov = []
    for temp2 in temp:
        if temp2 !='':
            temp2 = temp2.split(',')
            temp2 = [int(temp2[0]),int(temp2[1])]
            mov.append(temp2)
    user.append(mov)
    users.append(user)
cur.close()
conn.close()

userNum = len(users)
# print(userNum)
#浏览者用户数据

viewer = [userNum+1, [[241, 1], [201, 1], [75, 1], [63, 3], [142, 5], [91, 4], [213, 2]]]


# 得到相似喜好用户数据
def get_similarUsers():
    # 自定义比较函数
    def compare_personal(x, y):
        if x[2] != y[2]:
            return y[2] - x[2]
        else:
            return x[3] - y[3]


    #相似的用户
    similarUsers = []
    #参观者打过分的电影
    viewerMovDict = dict(viewer[1])
    viewerMovSet = set(dict(viewer[1]).keys())
    # print(viewerMovSet)
    for user in users:
        #定义一个similaUser
        similarUser = []
        similarUser.append(user[0])
        # 用户打过分的电影
        userMovDict = dict(user[1])
        userMovSet = set(userMovDict.keys())
        #跟参观者都打分的电影 求交集
        sameMov = list(userMovSet.intersection(viewerMovSet))
        similarUser.append(sameMov)
        similarUser.append(len(sameMov))
        # print(similarUser)
        # 相同电影打分的平均差

        if len(sameMov) == 0:
            similarUser.pop()
            similarUser.pop()
            continue
        else:
            sum = 0
            for same in sameMov:
                sum = sum + abs(viewerMovDict[same] - userMovDict[same])
            difference = sum/(len(sameMov))
        similarUser.append(difference)
        similarUsers.append(similarUser)
    #对得到的原始数据进行排序
    similarUsers = sorted(similarUsers, key=functools.cmp_to_key(compare_personal), reverse=False)
    # 参观者没看过而最相似用户看过的电影 差集
    viewerMovSee = list(set(dict(users[similarUsers[0][0]-1][1]).keys()).difference(set(similarUsers[0][1])))
    similarUsers[0].append(viewerMovSee)
    return similarUsers[0]

similarlestUser = get_similarUsers()


movies = []
conn = sqlite3.connect("movie.db")
cur = conn.cursor()
sql = "select * from doubanmovie250"
data = cur.execute(sql)
for item in data:
   movies.append(item)
cur.close()
conn.close()
print(similarlestUser)
print('和你最相似的用户是第%d号，你们喜欢相同的电影有%d部，评分平均差为%f'%(similarlestUser[0],similarlestUser[2],similarlestUser[3]))
print('向你推荐电影：')
for i in similarlestUser[4]:
    print(movies[i][3])



users = []



# for i in range(1,10):
#     user = []
#     #用户id
#     user.append(i)
#     movies=[]
#     #用户看过的电影(随机看过3到20部电影)
#     for ran in range(random.randint(3,20)):
#         movie = []
#         #随机生成id
#         random_movie_id = random.randint(1,251)
#         #随机生成评分
#         random_movie_rate = random.randint(1,5)
#         movie.append(random_movie_id)
#         movie.append(random_movie_rate)
#         movies.append(movie)
#     user.append(movies)
#     users.append(user)
#     print(user)

#
#
conn = sqlite3.connect("movie.db")
cur = conn.cursor()
sql3 = "drop table userData"
cur.execute(sql3)
sql1 = '''create table userData
(
    id            integer,
    userMov_Id_Rate     text
);'''

data = cur.execute(sql1)

for i in users:
    # print(i)
    userId = i[0]
    print(userId)
    strmov = ''
    for movie in i[1]:
        strmov = strmov+'|'+str(movie[0])+','+str(movie[1])
    strmov = "'"+strmov+"'"
    print(strmov)
    sql4 = 'insert into userData(id,userMov_Id_Rate) values (%d,%s)'%(userId,strmov)


    data = cur.execute(sql4)

    conn.commit()

# for i in data:
#     print(i)

cur.close()
conn.close()
