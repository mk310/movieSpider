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

# 影片的详情链接
findLink = re.compile(r'<a href="(.*?)">')  # 创建表达式对象，表示字符串匹配规则
# 影片的图片
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S忽略换行符
# 影片的片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片的评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 影片的评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
findDirector = re.compile(r'导演:(.*?)\u00a0',re.S)
findActor = re.compile('主演:(.*?)...<br/>',re.S)
findYear = re.compile('\d{4}',re.S)
findCountry = re.compile(r'/\u00a0(.*?)\s',re.S)
findMovietype = re.compile('/\u00a0(.*?)\n')

def main():
    #1爬取网页
    baseurl = "https://movie.douban.com/top250?start=0"
    datalist = getData(baseurl)
    print(datalist)

    #2解析数据
    #3保存数据
    # savapath = "豆瓣电影250.xls"
    # savaData(datalist,savapath)


    dbpath = 'movie.db'
    saveDatatoDb(datalist,dbpath)






#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i * 25)
        html = askUrl(url)

        #逐一对网页信息进行解析（使用beautifulsoup）
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            #查找符合要求的字符串，形成列表
            data = []                                           #保存一部电影的所有信息
            item_p=str(item.p)                                  #定位到item的p标签
            item = str(item)
            # 2找到电影的豆瓣链接
            link = re.findall(findLink,item)[0]                 #a按照find Link的规则查找itemd的第一个
            data.append(link)
            # 3找到电影图片链接
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            # 4找到电影标题
            title = re.findall(findTitle,item)                  #片名可能只有中文 没有外文的 也可能都有
            if(len(title)==2):                                  #有两个名字
                ctitle = title[0]
                data.append(ctitle)
                otitle = title[1].replace('/','')               #去除无关字符
                otitle = otitle.replace("\u00a0", "")           # 替换&nbsp
                data.append(otitle)
            else: #仅有一个
                data.append(title[0])
                data.append('')                                 #外文名留空
            # 5找到电影评分
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            # 6找到电影评价人数
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)
            # 7找到电影一句话
            inq = re.findall(findInq,item)
            if(len(inq) != 0):
                inq = inq[0].replace('。','')
                data.append(inq)
            else:
                data.append('')
            # 8找到电影的导演
            director = re.findall(findDirector,item_p)[0]
            # print(director)
            data.append(director)
            # 9找到电影的主演
            actor = re.findall(findActor,item_p)
            if len(actor)==0:
                data.append('')
            else:
                actor = actor[0]
                actor = re.sub('/', " ", actor)  # 替换/
                data.append(actor)
            # print(actor)
            #10找到电影上映年份
            year = re.findall(findYear,item_p)[0]
            # print(year)
            data.append(year.strip())
            #11 找到电影的地区
            country = re.findall(findCountry,item_p)[0]
            # print(country)
            data.append(country.strip())
            #12 找到电影的类型
            mvtype = re.findall(findMovietype,item_p)[0]
            mvtype = mvtype.split('/')[1].replace("\u00a0", "")                  #将爬取的信息按/分割,并且删除空格
            mvtype = mvtype.split(' ')                                           #将分割后的信息再按空格分割，作为列表
            mvtypes = ''
            for i in range(0,len(mvtype)):
                mvtypes = mvtypes+'|'+mvtype[i]
            print(mvtypes)
            data.append(mvtypes)



            datalist.append(data)


    return datalist

#得到指定url的网页内容
def askUrl(url):
    head = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36 Edg/98.0.1108.62",
            "Cookie":"acw_tc=7b39758216478597602756275e41bcf2993a64feeeaa69415588bd4539697a; channel=1300100141; device_id=web_SJ_EdRrzq; xq_a_token=1a689518b1d635a6b7d0b305d73548a29e3a5695; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1647859779; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1647859779; timestamp=1647860484049"}
    #用户代理，告诉服务器我是什么机器 能接受什么信息

    request = urllib.request.Request(url,headers=head)              #封装请求信息
    html = ""
    try:
        reponse = urllib.request.urlopen(request)                   #发出请求收到回应
        html = reponse.read().decode("utf-8") #读取获取的信息，格式为utf-8
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e.reason):
            print(e.reason)
    return html                                                     #返回网页信息

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
                insert into doubanmovie250 (
                info_link,pic_link,cname,ename,score,rated,instroduction,director,actor,year,country,mvtype)
                values(%s)'''%",".join(data)
        # print(sql) #测试用 输出sql语句
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print('数据存入数据库')

#数据库初始化
def initDb(dbpath):
    sql = '''
        create table doubanmovie250  
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