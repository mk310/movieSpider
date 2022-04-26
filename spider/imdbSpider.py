# -*- coding = utf-8 -*-
# @Time: 2022/3/2 16:49
# @Author: mk310
# @File: Spider.py
# @Software:PyCharm

import bs4 #网页解析，获取数据
from bs4 import BeautifulSoup
import re #正则表达式，进行文字匹配
import xlwt #Excel操作
import sqlite3 #数据库操作
import urllib.request,urllib.error #制定Url 获取网页数据

# 影片的第一层详情链接
findfirstLink = re.compile(r'<a href="(.*?)" target="_blank">')  # 创建表达式对象，表示字符串匹配规则
# 影片的图片
findImgSrc = re.compile(r'onerror="this.(.*?)>', re.S)  # re.S忽略换行符
# 影片的片名
findTitle = re.compile(r'content="(.*?),影评,简介,剧情,图片,评分,视频,影讯')
# 影片的评分
findRating = re.compile(r'<span><em class="Z_grade_rate">(.*?)</em>')
# 影片的评价人数
findJudge = re.compile(r'title="(.*?)人参与评分">')
# 找到概况
findInq = re.compile(r'<div class="profile_con" id="movie_desc_content" style="max-height: 200px;overflow: hidden">\n<p>(.*?)</p>',re.S)
# 找到相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
findDirector = re.compile(r'''导演：</div>\n<div class="txt_bottom_r txt_bottom_r_overflow">\n<a href="/name/(.*?)</a>''',re.S)
findActor = re.compile(r'主演：</div>\n<div class="txt_bottom_r txt_bottom_r_overflow">\n<a href="/name/(.*?)</a>',re.S)
findYear = re.compile(r'上映日期：</b>\n<span>(.*?)</span>',re.S)
findCountry = re.compile(r'制片国家/地区：</div>\n<div class="txt_bottom_r">(.*?)</div>',re.S)
findMovietype = re.compile(r'类型：</div>\n<div class="txt_bottom_r">(.*?)</div>',re.S)

def main():
    #1爬取网页
    baseurl = "https://www.iyingku.cn/imdb250/order/rate/sort/desc"
    datalist = getData(baseurl)
    print(datalist)



    #2解析数据
    #3保存数据
    # savapath = "idmb250.xls"
    # savaData(datalist,savapath)


    dbpath = 'movie.db'
    saveDatatoDb(datalist,dbpath)





#保存数据到excel
def savaData(datalist,savepath):
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet('豆瓣电影',cell_overwrite_ok=True)            # 创建工作表(特性为单元格可以覆写)
    col = ("电影链接","图片链接","中文名","外文名","评分","评价人数","概况","导演","演员","年份","地区")
    for i in range(1,11):
        worksheet.write(0,i,col[i])                                             #表单的第一行名称
    for i in range(0,250):
        print("爬取第%d次"%(i+1))
        data = datalist[i]
        for j in range(0,11):
            worksheet.write(i+1,j,data[j])
    workbook.save(savepath)



#爬取网页
def getData(baseurl):
    datalist = []
    secondbaseLink = 'https://www.iyingku.cn'
    #返回第一页的html
    firsthtml = askUrl(baseurl)
    #逐一对网页信息进行解析（使用beautifulsoup）
    soup = BeautifulSoup(firsthtml,"html.parser")

    count = 1                                   #去除第一个无用数据的标志
    for item in soup.find_all('tr',class_=""):  #找到所有含数据的标签字段
        data = []
        if count == 1:
            count = 0
            continue                            #去除第一个无用的字段
        item = str(item)                        #将数据字符化

        firstlink = re.findall(findfirstLink,item)[0]     #找到第步链接的尾端

        secondlink = secondbaseLink + firstlink             #组合 得到第二步的链接

        secondhtml = askUrl(secondlink)
        # 逐一对网页信息进行解析（使用beautifulsoup）
        secondesoup = BeautifulSoup(secondhtml, "html.parser")
        item2 = str(secondesoup)
        # print(item2)
        # 2电影详情页面链接
        data.append(secondlink)

        # 3找到电影图片链接
        imgSrc = re.findall(findImgSrc, item2)[0]

        imgSrc = imgSrc.split('src=')[2]  # 对接受的信息截取第二个链接
        imgSrc = imgSrc.replace("\"", "")  # 去掉链接的引号
        data.append(imgSrc)

        # 4找到电影标题
        title = re.findall(findTitle, item2)[0]  # 片名可能只有中文 没有外文的 也可能都有
        title = title.split(",")
        if (len(title) == 2):  # 有两个名字
            ctitle = title[0]
            data.append(ctitle)
            otitle = title[1]
            data.append(otitle)
        else:  # 仅有一个
            data.append(title[0])
            data.append('')  # 外文名留空
        # 5找到电影评分
        rating = re.findall(findRating, item2)[0]
        data.append(rating)
        # 6找到电影评价人数
        judgeNum = re.findall(findJudge, item2)[0]
        data.append(judgeNum)
        # 7找到电影一句话
        inq = re.findall(findInq, item2)
        if len(inq) != 0:
            inq = inq[0].strip().replace('。', '')  # 去掉空格 句号
            inq = inq.replace('\"'," ")
            data.append(inq)
        else:
            data.append('xiangwangrangren ')
        # 8找到电影的导演
        director = re.findall(findDirector, item2)[0]
        director = director.split('>')[1]
        data.append(director)
        # 9找到电影的主演
        actor = re.findall(findActor, item2)
        if len(actor) == 0:
            data.append('')
        else:
            actor = actor[0].split(">")[1]
            actor = re.sub('/', " ", actor)  # 替换/
            data.append(actor)
        # 10找到电影上映年份
        year = re.findall(findYear, item2)
        if len(year) == 0:
            data.append('3033')
        else:
            data.append(year[0].strip())
        # 11 找到电影的地区
        country = re.findall(findCountry, item2)[0]
        country = country.split('/')[0]
        data.append(country.strip())
        # 12 找到电影的类型
        mvtype = re.findall(findMovietype, item2)
        if len(mvtype) == 0:
            data.append('train')
        else:
            mvtype = mvtype[0].replace('/', '|')
            mvtype = mvtype.replace(" ", '')
            data.append(mvtype.strip())
        print(data)
        datalist.append(data)
    return datalist
    print('成功获取数据datalist')

#得到指定url的网页内容
def askUrl(url):
    head = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36 Edg/98.0.1108.62",
            "Cookie":"acw_tc=7b39758216478597602756275e41bcf2993a64feeeaa69415588bd4539697a; channel=1300100141; device_id=web_SJ_EdRrzq; xq_a_token=1a689518b1d635a6b7d0b305d73548a29e3a5695; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1647859779; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1647859779; timestamp=1647860484049"}
    #用户代理，告诉服务器我是什么机器 能接受什么信息

    request = urllib.request.Request(url,headers=head)              #封装请求信息
    html = ""
    try:
        reponse = urllib.request.urlopen(request)                   #发出请求收到回应
        html = reponse.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e.reason):
            print(e.reason)
    return html                                                     #返回网页信息
    print('成功获得网页html信息')

#保存数据到数据库
def saveDatatoDb(datalist,dbpath):
    initDb(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5 or index == 9:
                continue
            data[index]='"'+str(data[index])+'"'
        sql = '''
                insert into imdbmovie250 (
                info_link,pic_link,cname,ename,score,rated,instroduction,director,actor,year,country,mvtype)
                values(%s)'''%",".join(data)
        # print(sql) #测试用 输出sql语句
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print('数据存入数据库完成')

#数据库初始化
def initDb(dbpath):
    sql = '''
        create table imdbmovie250  
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename  varchar,
        score numeric,
        rated  numeric,
        instroduction text,
        director text,
        actor text,
        year numeric,
        country text,
        mvtype text
        )
    '''    #创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print('创建数据库完毕')

if __name__ == "__main__":          #当程序执行时
#调用函数
     main()
     # initDb("movietest.db")
     print("爬取完毕！")