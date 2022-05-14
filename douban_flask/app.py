from flask import Flask,render_template
import sqlite3
from flask import request,redirect,url_for
import time
#生成随机数
import random
import functools

app = Flask(__name__)




@app.route('/')
def index():  # put application's code here
    msg = '待操作'
    logusers = []
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sqlall = "select * from userlog "
    allusers = cur.execute(sqlall)
    for uer in allusers:
        user = []
        user.append(uer[0])
        user.append(uer[2])
        logusers.append(user)
    cur.close()
    conn.close()

    return render_template("login.html",msg = msg,logusers = logusers)  #默认指向templates


@app.route('/login', methods=['POST'])
def login():
    passwordu = 0
    length = 0
    logusers = []
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sqlall = "select * from userlog "
    allusers = cur.execute(sqlall)
    for uer in allusers:
        user = []
        user.append(uer[0])
        user.append(uer[2])
        logusers.append(user)

    username = request.form.get('username')
    password = request.form.get('pwd')


    #后台登录
    if username == 'sudo' and password == '123':
        return render_template("backin.html",logusers = logusers)
    #不能为空
    if username == ''or password == '':
        return render_template("login.html", msg="密码或者用户名不能为空",logusers =logusers)
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sqluser = "select password,date from userlog where user = '%s'" % (username)
    userpasses = cur.execute(sqluser)
    for userpass in userpasses:
        length = len(userpass)
        passwordu = userpass[0]




   #输入的用户不存在，直接注册
    if length == 0:

        date= time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        date = "'" + date + "'"
        sqlinsert = '''
                       insert into userlog (user,password,date)
                       values('%s','%s',%s)'''%(username,password,date)
        cur.execute(sqlinsert)
        conn.commit()
        logusers = []
        sqlall = "select * from userlog "
        allusers = cur.execute(sqlall)
        for uer in allusers:
            user = []
            user.append(uer[0])
            user.append(uer[2])
            logusers.append(user)

        return render_template("login.html", msg="用户不存在,现已注册,请登录",logusers = logusers)

    if password == passwordu:
        return render_template("index.html", msg="登录成功")
    else:
        return render_template("login.html", msg="密码错误",logusers = logusers)

    cur.close()
    conn.close()

#后台
@app.route('/backin')
def backin():
    passwordu = 0
    length = 0
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

    return render_template("back.html",logusers =logusers)





#后台
@app.route('/back',methods=['GET','POST'])
def back():
    passwordu = 0
    length = 0
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

    username = request.form.get('username')
    password = request.form.get('pwd')
    # 用户不存在
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sqluser = "select password,date from userlog where user = '%s'" % (username)
    userpasses = cur.execute(sqluser)
    for userpass in userpasses:
        length = len(userpass)
    if length == 0:
        return render_template("back.html", msg="用户不存在", logusers =logusers)
    # 用户存在
    else:
        # 删除
        if password== 'del':
            sqlde = "DELETE FROM userlog WHERE user = '%s'" % (username)
            cur.execute(sqlde)
            conn.commit()
            logusers = []
            sqlall = "select * from userlog "
            allusers = cur.execute(sqlall)
            for uer in allusers:
                user = []
                user.append(uer[0])
                user.append(uer[1])
                user.append(uer[2])
                logusers.append(user)

            return render_template("back.html", msg="删除",logusers =logusers)
        else:
            sqlup = "UPDATE userlog SET password = '%s' WHERE user = '%s'" % (password, username)
            cur.execute(sqlup)
            conn.commit()
            logusers = []
            sqlall = "select * from userlog "
            allusers = cur.execute(sqlall)
            for uer in allusers:
                user = []
                user.append(uer[0])
                user.append(uer[1])
                user.append(uer[2])
                logusers.append(user)
            return render_template("back.html", msg="修改密码", logusers =logusers)
    return render_template("back.html", msg="待操作", logusers =logusers)

    # else:
    #     if password == '':

    #     else:

    #
    #     conn = sqlite3.connect("movie.db")
    #     cur = conn.cursor()
    #     sqlall = "select * from userlog "
    #     allusers = cur.execute(sqlall)
    #     for uer in allusers:
    #         user = []
    #         user.append(uer[0])
    #         user.append(uer[1])
    #         user.append(uer[2])
    #         logusers.append(user)
    #     return render_template("back.html", msg="修改后", logusers=logusers)








   #
   #  if password == passwordu:
   #      return render_template("index.html", msg="登录成功")
   #  else:
   #      return render_template("login.html", msg="密码错误",logusers = logusers)

    cur.close()
    conn.close()

#主页
@app.route('/index')
def home():
    return  render_template("index.html")

# imdb电影页面
@app.route('/imdbmovie')
def imdbmovie():
    datalist = []
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select * from imdbmovie250"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()
    return  render_template("imdbmovie.html",movies = datalist)


#imdb电影详情
@app.route('/imdbscore')
def imdbscore():
    score = []  #评分区间
    num = []  #评分统计数
    countryName = {'阿富汗': 'Afghanistan', '奥兰群岛': 'Aland Islands', '阿尔巴尼亚': 'Albania', '阿尔及利亚': 'Algeria',
                   '美属萨摩亚': 'American Samoa', '安道尔': 'Andorra', '安哥拉': 'Angola', '安圭拉': 'Anguilla',
                   '安提瓜和巴布达': 'Antigua and Barbuda', '阿根廷': 'Argentina', '亚美尼亚': 'Armenia', '阿鲁巴': 'Aruba',
                   '澳大利亚': 'Australia', '奥地利': 'Austria', '阿塞拜疆': 'Azerbaijan', '孟加拉': 'Bangladesh', '巴林': 'Bahrain',
                   '巴哈马': 'Bahamas', '巴巴多斯': 'Barbados', '白俄罗斯': 'Belarus', '比利时': 'Belgium', '伯利兹': 'Belize',
                   '贝宁': 'Benin', '百慕大': 'Bermuda', '不丹': 'Bhutan', '玻利维亚': 'Bolivia',
                   '波斯尼亚和黑塞哥维那': 'Bosnia and Herzegovina', '博茨瓦纳': 'Botswana', '布维岛': 'Bouvet Island', '巴西': 'Brazil',
                   '文莱': 'Brunei', '保加利亚': 'Bulgaria', '布基纳法索': 'Burkina Faso', '布隆迪': 'Burundi', '柬埔寨': 'Cambodia',
                   '喀麦隆': 'Cameroon', '加拿大': 'Canada', '佛得角': 'Cape Verde', '中非': 'Central African Republic',
                   '乍得': 'Chad', '智利': 'Chile', '圣诞岛': 'Christmas Islands', '科科斯（基林）群岛': 'Cocos (keeling) Islands',
                   '哥伦比亚': 'Colombia', '科摩罗': 'Comoros', '刚果（金）': 'Congo (Congo-Kinshasa)', '刚果': 'Congo',
                   '库克群岛': 'Cook Islands', '哥斯达黎加': 'Costa Rica', '科特迪瓦': 'Cote D’Ivoire', '中国大陆': 'China',
                   '克罗地亚': 'Croatia', '古巴': 'Cuba', '捷克': 'Czech', '塞浦路斯': 'Cyprus', '丹麦': 'Denmark', '吉布提': 'Djibouti',
                   '多米尼加': 'Dominica', '东帝汶': 'Timor-Leste', '厄瓜多尔': 'Ecuador', '埃及': 'Egypt',
                   '赤道几内亚': 'Equatorial Guinea', '厄立特里亚': 'Eritrea', '爱沙尼亚': 'Estonia', '埃塞俄比亚': 'Ethiopia',
                   '法罗群岛': 'Faroe Islands', '斐济': 'Fiji', '芬兰': 'Finland', '法国': 'France',
                   '法国大都会': 'Franch Metropolitan', '法属圭亚那': 'Franch Guiana', '法属波利尼西亚': 'French Polynesia',
                   '加蓬': 'Gabon', '冈比亚': 'Gambia', '格鲁吉亚': 'Georgia', '德国': 'Germany', '加纳': 'Ghana',
                   '直布罗陀': 'Gibraltar', '希腊': 'Greece', '格林纳达': 'Grenada', '瓜德罗普岛': 'Guadeloupe', '关岛': 'Guam',
                   '危地马拉': 'Guatemala', '根西岛': 'Guernsey', '几内亚比绍': 'Guinea-Bissau', '几内亚': 'Guinea', '圭亚那': 'Guyana',
                   '中国香港': 'Hong Kong', '海地': 'Haiti', '洪都拉斯': 'Honduras', '匈牙利': 'Hungary', '冰岛': 'Iceland',
                   '印度': 'India', '印度尼西亚': 'Indonesia', '伊朗': 'Iran', '伊拉克': 'Iraq', '爱尔兰': 'Ireland',
                   '马恩岛': 'Isle of Man', '以色列': 'Israel', '意大利': 'Italy', '牙买加': 'Jamaica', '日本': 'Japan',
                   '泽西岛': 'Jersey', '约旦': 'Jordan', '哈萨克斯坦': 'Kazakhstan', '肯尼亚': 'Kenya', '基里巴斯': 'Kiribati',
                   '韩国': 'South Korea', '朝鲜': 'Korea (North)', '科威特': 'Kuwait', '吉尔吉斯斯坦': 'Kyrgyzstan', '老挝': 'Laos',
                   '拉脱维亚': 'Latvia', '黎巴嫩': 'Lebanon', '莱索托': 'Lesotho', '利比里亚': 'Liberia', '利比亚': 'Libya',
                   '列支敦士登': 'Liechtenstein', '立陶宛': 'Lithuania', '卢森堡': 'Luxembourg', '中国澳门': 'Macau',
                   '马其顿': 'Macedonia', '马拉维': 'Malawi', '马来西亚': 'Malaysia', '马达加斯加': 'Madagascar', '马尔代夫': 'Maldives',
                   '马里': 'Mali', '马耳他': 'Malta', '马绍尔群岛': 'Marshall Islands', '马提尼克岛': 'Martinique',
                   '毛里塔尼亚': 'Mauritania', '毛里求斯': 'Mauritius', '马约特': 'Mayotte', '墨西哥': 'Mexico',
                   '密克罗尼西亚': 'Micronesia', '摩尔多瓦': 'Moldova', '摩纳哥': 'Monaco', '蒙古': 'Mongolia', '黑山': 'Montenegro',
                   '蒙特塞拉特': 'Montserrat', '摩洛哥': 'Morocco', '莫桑比克': 'Mozambique', '缅甸': 'Myanmar', '纳米比亚': 'Namibia',
                   '瑙鲁': 'Nauru', '尼泊尔': 'Nepal', '荷兰': 'Netherlands', '新喀里多尼亚': 'New Caledonia', '新西兰': 'New Zealand',
                   '尼加拉瓜': 'Nicaragua', '尼日尔': 'Niger', '尼日利亚': 'Nigeria', '纽埃': 'Niue', '诺福克岛': 'Norfolk Island',
                   '挪威': 'Norway', '阿曼': 'Oman', '巴基斯坦': 'Pakistan', '帕劳': 'Palau', '巴勒斯坦': 'Palestine',
                   '巴拿马': 'Panama', '巴布亚新几内亚': 'Papua New Guinea', '巴拉圭': 'Paraguay', '秘鲁': 'Peru',
                   '菲律宾': 'Philippines', '皮特凯恩群岛': 'Pitcairn Islands', '波兰': 'Poland', '葡萄牙': 'Portugal',
                   '波多黎各': 'Puerto Rico', '卡塔尔': 'Qatar', '留尼汪岛': 'Reunion', '罗马尼亚': 'Romania', '卢旺达': 'Rwanda',
                   '俄罗斯联邦': 'Russian Federation', '圣赫勒拿': 'Saint Helena', '圣基茨和尼维斯': 'Saint Kitts-Nevis',
                   '圣卢西亚': 'Saint Lucia', '圣文森特和格林纳丁斯': 'Saint Vincent and the Grenadines', '萨尔瓦多': 'El Salvador',
                   '萨摩亚': 'Samoa', '圣马力诺': 'San Marino', '圣多美和普林西比': 'Sao Tome and Principe', '沙特阿拉伯': 'Saudi Arabia',
                   '塞内加尔': 'Senegal', '塞舌尔': 'Seychelles', '塞拉利昂': 'Sierra Leone', '新加坡': 'Singapore', '塞尔维亚': 'Serbia',
                   '斯洛伐克': 'Slovakia', '斯洛文尼亚': 'Slovenia', '所罗门群岛': 'Solomon Islands', '索马里': 'Somalia',
                   '南非': 'South Africa', '西班牙': 'Spain', '斯里兰卡': 'Sri Lanka', '苏丹': 'Sudan', '苏里南': 'Suriname',
                   '斯威士兰': 'Swaziland', '瑞典': 'Sweden', '瑞士': 'Switzerland', '叙利亚': 'Syria', '塔吉克斯坦': 'Tajikistan',
                   '坦桑尼亚': 'Tanzania', '中国台湾': 'Taiwan', '泰国': 'Thailand', '特立尼达和多巴哥': 'Trinidad and Tobago',
                   '多哥': 'Togo', '托克劳': 'Tokelau', '汤加': 'Tonga', '突尼斯': 'Tunisia', '土耳其': 'Turkey',
                   '土库曼斯坦': 'Turkmenistan', '图瓦卢': 'Tuvalu', '乌干达': 'Uganda', '乌克兰': 'Ukraine',
                   '阿拉伯联合酋长国': 'United Arab Emirates', '英国': 'United Kingdom', '美国': 'United States of America', '乌拉圭': 'Uruguay',
                   '乌兹别克斯坦': 'Uzbekistan', '瓦努阿图': 'Vanuatu', '梵蒂冈': 'Vatican City', '委内瑞拉': 'Venezuela',
                   '越南': 'Vietnam', '瓦利斯群岛和富图纳群岛': 'Wallis and Futuna', '西撒哈拉': 'Western Sahara', '也门': 'Yemen',
                   '南斯拉夫': 'Yugoslavia', '赞比亚': 'Zambia', '津巴布韦': 'Zimbabwe'}
    country = []   #国家
    year = []    #电影发兴年份
    yearnum = []  #年份数量
    mvtype = [] #电影类型
    mvtypenum  = []  #类型数量
    mvtypedata = []  #电影类型数据
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select score,count(score) from imdbmovie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(item[1])
    sql2 = "select country,count(country) from imdbmovie250 group by country"  #得到国家电影数目的数据
    data2 = cur.execute(sql2)
    for item in data2:
        country.append(item)
    sql3 = "select year,count(year) from imdbmovie250 group by year"  # 得到国家电影数目的数据
    data3 = cur.execute(sql3)
    for item in data2:
        year.append(item[0])
        yearnum.append(item[1])
    sql4 = "select mvtype from imdbmovie250 "  # 得到国家电影数目的数据
    data4 = cur.execute(sql4)
    for i in data4:
        data = i[0].split("|")
        for e in data:
            mvtypedata.append(e)
    mvtypedata = sorted(mvtypedata)
    for i in range(1, len(mvtypedata)):
        if mvtypedata[i] != mvtypedata[i - 1]:
            mvtype.append(mvtypedata[i])
    for mov in mvtype:
        mvtypenum.append(mvtypedata.count(mov))
    cur.close()
    conn.close()
    length  = len(mvtype)




    return  render_template("imdbscore.html",score = score,num = num,country = country,countryName = countryName,year =year,yearnum = yearnum,mvtypenum = mvtypenum,mvtype = mvtype,length = length)

#豆瓣电影界面
@app.route('/doubanmovie')
def doubanmovie():
    datalist = []
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select * from doubanmovie250"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()
    return  render_template("doubanmovie.html",movies = datalist)


#豆瓣电影详情界面
@app.route('/doubanscore')
def doubanscore():
    score = []  #评分区间
    num = []  #评分统计数
    countryName = {'阿富汗': 'Afghanistan', '奥兰群岛': 'Aland Islands', '阿尔巴尼亚': 'Albania', '阿尔及利亚': 'Algeria',
                   '美属萨摩亚': 'American Samoa', '安道尔': 'Andorra', '安哥拉': 'Angola', '安圭拉': 'Anguilla',
                   '安提瓜和巴布达': 'Antigua and Barbuda', '阿根廷': 'Argentina', '亚美尼亚': 'Armenia', '阿鲁巴': 'Aruba',
                   '澳大利亚': 'Australia', '奥地利': 'Austria', '阿塞拜疆': 'Azerbaijan', '孟加拉': 'Bangladesh', '巴林': 'Bahrain',
                   '巴哈马': 'Bahamas', '巴巴多斯': 'Barbados', '白俄罗斯': 'Belarus', '比利时': 'Belgium', '伯利兹': 'Belize',
                   '贝宁': 'Benin', '百慕大': 'Bermuda', '不丹': 'Bhutan', '玻利维亚': 'Bolivia',
                   '波斯尼亚和黑塞哥维那': 'Bosnia and Herzegovina', '博茨瓦纳': 'Botswana', '布维岛': 'Bouvet Island', '巴西': 'Brazil',
                   '文莱': 'Brunei', '保加利亚': 'Bulgaria', '布基纳法索': 'Burkina Faso', '布隆迪': 'Burundi', '柬埔寨': 'Cambodia',
                   '喀麦隆': 'Cameroon', '加拿大': 'Canada', '佛得角': 'Cape Verde', '中非': 'Central African Republic',
                   '乍得': 'Chad', '智利': 'Chile', '圣诞岛': 'Christmas Islands', '科科斯（基林）群岛': 'Cocos (keeling) Islands',
                   '哥伦比亚': 'Colombia', '科摩罗': 'Comoros', '刚果（金）': 'Congo (Congo-Kinshasa)', '刚果': 'Congo',
                   '库克群岛': 'Cook Islands', '哥斯达黎加': 'Costa Rica', '科特迪瓦': 'Cote D’Ivoire', '中国大陆': 'China',
                   '克罗地亚': 'Croatia', '古巴': 'Cuba', '捷克': 'Czech', '塞浦路斯': 'Cyprus', '丹麦': 'Denmark', '吉布提': 'Djibouti',
                   '多米尼加': 'Dominica', '东帝汶': 'Timor-Leste', '厄瓜多尔': 'Ecuador', '埃及': 'Egypt',
                   '赤道几内亚': 'Equatorial Guinea', '厄立特里亚': 'Eritrea', '爱沙尼亚': 'Estonia', '埃塞俄比亚': 'Ethiopia',
                   '法罗群岛': 'Faroe Islands', '斐济': 'Fiji', '芬兰': 'Finland', '法国': 'France',
                   '法国大都会': 'Franch Metropolitan', '法属圭亚那': 'Franch Guiana', '法属波利尼西亚': 'French Polynesia',
                   '加蓬': 'Gabon', '冈比亚': 'Gambia', '格鲁吉亚': 'Georgia', '德国': 'Germany', '加纳': 'Ghana',
                   '直布罗陀': 'Gibraltar', '希腊': 'Greece', '格林纳达': 'Grenada', '瓜德罗普岛': 'Guadeloupe', '关岛': 'Guam',
                   '危地马拉': 'Guatemala', '根西岛': 'Guernsey', '几内亚比绍': 'Guinea-Bissau', '几内亚': 'Guinea', '圭亚那': 'Guyana',
                   '中国香港': 'Hong Kong', '海地': 'Haiti', '洪都拉斯': 'Honduras', '匈牙利': 'Hungary', '冰岛': 'Iceland',
                   '印度': 'India', '印度尼西亚': 'Indonesia', '伊朗': 'Iran', '伊拉克': 'Iraq', '爱尔兰': 'Ireland',
                   '马恩岛': 'Isle of Man', '以色列': 'Israel', '意大利': 'Italy', '牙买加': 'Jamaica', '日本': 'Japan',
                   '泽西岛': 'Jersey', '约旦': 'Jordan', '哈萨克斯坦': 'Kazakhstan', '肯尼亚': 'Kenya', '基里巴斯': 'Kiribati',
                   '韩国': 'South Korea', '朝鲜': 'Korea (North)', '科威特': 'Kuwait', '吉尔吉斯斯坦': 'Kyrgyzstan', '老挝': 'Laos',
                   '拉脱维亚': 'Latvia', '黎巴嫩': 'Lebanon', '莱索托': 'Lesotho', '利比里亚': 'Liberia', '利比亚': 'Libya',
                   '列支敦士登': 'Liechtenstein', '立陶宛': 'Lithuania', '卢森堡': 'Luxembourg', '中国澳门': 'Macau',
                   '马其顿': 'Macedonia', '马拉维': 'Malawi', '马来西亚': 'Malaysia', '马达加斯加': 'Madagascar', '马尔代夫': 'Maldives',
                   '马里': 'Mali', '马耳他': 'Malta', '马绍尔群岛': 'Marshall Islands', '马提尼克岛': 'Martinique',
                   '毛里塔尼亚': 'Mauritania', '毛里求斯': 'Mauritius', '马约特': 'Mayotte', '墨西哥': 'Mexico',
                   '密克罗尼西亚': 'Micronesia', '摩尔多瓦': 'Moldova', '摩纳哥': 'Monaco', '蒙古': 'Mongolia', '黑山': 'Montenegro',
                   '蒙特塞拉特': 'Montserrat', '摩洛哥': 'Morocco', '莫桑比克': 'Mozambique', '缅甸': 'Myanmar', '纳米比亚': 'Namibia',
                   '瑙鲁': 'Nauru', '尼泊尔': 'Nepal', '荷兰': 'Netherlands', '新喀里多尼亚': 'New Caledonia', '新西兰': 'New Zealand',
                   '尼加拉瓜': 'Nicaragua', '尼日尔': 'Niger', '尼日利亚': 'Nigeria', '纽埃': 'Niue', '诺福克岛': 'Norfolk Island',
                   '挪威': 'Norway', '阿曼': 'Oman', '巴基斯坦': 'Pakistan', '帕劳': 'Palau', '巴勒斯坦': 'Palestine',
                   '巴拿马': 'Panama', '巴布亚新几内亚': 'Papua New Guinea', '巴拉圭': 'Paraguay', '秘鲁': 'Peru',
                   '菲律宾': 'Philippines', '皮特凯恩群岛': 'Pitcairn Islands', '波兰': 'Poland', '葡萄牙': 'Portugal',
                   '波多黎各': 'Puerto Rico', '卡塔尔': 'Qatar', '留尼汪岛': 'Reunion', '罗马尼亚': 'Romania', '卢旺达': 'Rwanda',
                   '俄罗斯联邦': 'Russian Federation', '圣赫勒拿': 'Saint Helena', '圣基茨和尼维斯': 'Saint Kitts-Nevis',
                   '圣卢西亚': 'Saint Lucia', '圣文森特和格林纳丁斯': 'Saint Vincent and the Grenadines', '萨尔瓦多': 'El Salvador',
                   '萨摩亚': 'Samoa', '圣马力诺': 'San Marino', '圣多美和普林西比': 'Sao Tome and Principe', '沙特阿拉伯': 'Saudi Arabia',
                   '塞内加尔': 'Senegal', '塞舌尔': 'Seychelles', '塞拉利昂': 'Sierra Leone', '新加坡': 'Singapore', '塞尔维亚': 'Serbia',
                   '斯洛伐克': 'Slovakia', '斯洛文尼亚': 'Slovenia', '所罗门群岛': 'Solomon Islands', '索马里': 'Somalia',
                   '南非': 'South Africa', '西班牙': 'Spain', '斯里兰卡': 'Sri Lanka', '苏丹': 'Sudan', '苏里南': 'Suriname',
                   '斯威士兰': 'Swaziland', '瑞典': 'Sweden', '瑞士': 'Switzerland', '叙利亚': 'Syria', '塔吉克斯坦': 'Tajikistan',
                   '坦桑尼亚': 'Tanzania', '中国台湾': 'Taiwan', '泰国': 'Thailand', '特立尼达和多巴哥': 'Trinidad and Tobago',
                   '多哥': 'Togo', '托克劳': 'Tokelau', '汤加': 'Tonga', '突尼斯': 'Tunisia', '土耳其': 'Turkey',
                   '土库曼斯坦': 'Turkmenistan', '图瓦卢': 'Tuvalu', '乌干达': 'Uganda', '乌克兰': 'Ukraine',
                   '阿拉伯联合酋长国': 'United Arab Emirates', '英国': 'United Kingdom', '美国': 'United States of America', '乌拉圭': 'Uruguay',
                   '乌兹别克斯坦': 'Uzbekistan', '瓦努阿图': 'Vanuatu', '梵蒂冈': 'Vatican City', '委内瑞拉': 'Venezuela',
                   '越南': 'Vietnam', '瓦利斯群岛和富图纳群岛': 'Wallis and Futuna', '西撒哈拉': 'Western Sahara', '也门': 'Yemen',
                   '南斯拉夫': 'Yugoslavia', '赞比亚': 'Zambia', '津巴布韦': 'Zimbabwe'}
    country = []   #国家
    year = []    #电影发兴年份
    yearnum = []  #年份数量
    mvtype = [] #电影类型
    mvtypenum  = []  #类型数量
    mvtypedata = []  #电影类型数据
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select score,count(score) from doubanmovie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(item[1])
    sql2 = "select country,count(country) from doubanmovie250 group by country"  #得到国家电影数目的数据
    data2 = cur.execute(sql2)
    for item in data2:
        country.append(item)
    sql3 = "select year,count(year) from doubanmovie250 group by year"  # 得到国家电影数目的数据
    data3 = cur.execute(sql3)
    for item in data2:
        year.append(item[0])
        yearnum.append(item[1])
    sql4 = "select mvtype from doubanmovie250 "  # 得到国家电影数目的数据
    data4 = cur.execute(sql4)
    for i in data4:
        data = i[0].split("|")
        for e in data:
            mvtypedata.append(e)
    mvtypedata = sorted(mvtypedata)
    for i in range(1, len(mvtypedata)):
        if mvtypedata[i] != mvtypedata[i - 1]:
            mvtype.append(mvtypedata[i])
    for mov in mvtype:
        mvtypenum.append(mvtypedata.count(mov))
    cur.close()
    conn.close()
    length  = len(mvtype)
    #翻译国家的英文名
    return  render_template("doubanscore.html",score = score,num = num,country = country,countryName = countryName,year =year,yearnum = yearnum,mvtypenum = mvtypenum,mvtype = mvtype,length = length)


countryUnio = []
# 电影数据对比界面
@app.route('/scorecompare')
def scorecompare():
    score = []  #评分区间
    num = []  #评分统计数
    countryName = {'阿富汗': 'Afghanistan', '奥兰群岛': 'Aland Islands', '阿尔巴尼亚': 'Albania', '阿尔及利亚': 'Algeria',
                   '美属萨摩亚': 'American Samoa', '安道尔': 'Andorra', '安哥拉': 'Angola', '安圭拉': 'Anguilla',
                   '安提瓜和巴布达': 'Antigua and Barbuda', '阿根廷': 'Argentina', '亚美尼亚': 'Armenia', '阿鲁巴': 'Aruba',
                   '澳大利亚': 'Australia', '奥地利': 'Austria', '阿塞拜疆': 'Azerbaijan', '孟加拉': 'Bangladesh', '巴林': 'Bahrain',
                   '巴哈马': 'Bahamas', '巴巴多斯': 'Barbados', '白俄罗斯': 'Belarus', '比利时': 'Belgium', '伯利兹': 'Belize',
                   '贝宁': 'Benin', '百慕大': 'Bermuda', '不丹': 'Bhutan', '玻利维亚': 'Bolivia',
                   '波斯尼亚和黑塞哥维那': 'Bosnia and Herzegovina', '博茨瓦纳': 'Botswana', '布维岛': 'Bouvet Island', '巴西': 'Brazil',
                   '文莱': 'Brunei', '保加利亚': 'Bulgaria', '布基纳法索': 'Burkina Faso', '布隆迪': 'Burundi', '柬埔寨': 'Cambodia',
                   '喀麦隆': 'Cameroon', '加拿大': 'Canada', '佛得角': 'Cape Verde', '中非': 'Central African Republic',
                   '乍得': 'Chad', '智利': 'Chile', '圣诞岛': 'Christmas Islands', '科科斯（基林）群岛': 'Cocos (keeling) Islands',
                   '哥伦比亚': 'Colombia', '科摩罗': 'Comoros', '刚果（金）': 'Congo (Congo-Kinshasa)', '刚果': 'Congo',
                   '库克群岛': 'Cook Islands', '哥斯达黎加': 'Costa Rica', '科特迪瓦': 'Cote D’Ivoire', '中国大陆': 'China',
                   '克罗地亚': 'Croatia', '古巴': 'Cuba', '捷克': 'Czech', '塞浦路斯': 'Cyprus', '丹麦': 'Denmark', '吉布提': 'Djibouti',
                   '多米尼加': 'Dominica', '东帝汶': 'Timor-Leste', '厄瓜多尔': 'Ecuador', '埃及': 'Egypt',
                   '赤道几内亚': 'Equatorial Guinea', '厄立特里亚': 'Eritrea', '爱沙尼亚': 'Estonia', '埃塞俄比亚': 'Ethiopia',
                   '法罗群岛': 'Faroe Islands', '斐济': 'Fiji', '芬兰': 'Finland', '法国': 'France',
                   '法国大都会': 'Franch Metropolitan', '法属圭亚那': 'Franch Guiana', '法属波利尼西亚': 'French Polynesia',
                   '加蓬': 'Gabon', '冈比亚': 'Gambia', '格鲁吉亚': 'Georgia', '德国': 'Germany', '加纳': 'Ghana',
                   '直布罗陀': 'Gibraltar', '希腊': 'Greece', '格林纳达': 'Grenada', '瓜德罗普岛': 'Guadeloupe', '关岛': 'Guam',
                   '危地马拉': 'Guatemala', '根西岛': 'Guernsey', '几内亚比绍': 'Guinea-Bissau', '几内亚': 'Guinea', '圭亚那': 'Guyana',
                   '中国香港': 'Hong Kong', '海地': 'Haiti', '洪都拉斯': 'Honduras', '匈牙利': 'Hungary', '冰岛': 'Iceland',
                   '印度': 'India', '印度尼西亚': 'Indonesia', '伊朗': 'Iran', '伊拉克': 'Iraq', '爱尔兰': 'Ireland',
                   '马恩岛': 'Isle of Man', '以色列': 'Israel', '意大利': 'Italy', '牙买加': 'Jamaica', '日本': 'Japan',
                   '泽西岛': 'Jersey', '约旦': 'Jordan', '哈萨克斯坦': 'Kazakhstan', '肯尼亚': 'Kenya', '基里巴斯': 'Kiribati',
                   '韩国': 'South Korea', '朝鲜': 'Korea (North)', '科威特': 'Kuwait', '吉尔吉斯斯坦': 'Kyrgyzstan', '老挝': 'Laos',
                   '拉脱维亚': 'Latvia', '黎巴嫩': 'Lebanon', '莱索托': 'Lesotho', '利比里亚': 'Liberia', '利比亚': 'Libya',
                   '列支敦士登': 'Liechtenstein', '立陶宛': 'Lithuania', '卢森堡': 'Luxembourg', '中国澳门': 'Macau',
                   '马其顿': 'Macedonia', '马拉维': 'Malawi', '马来西亚': 'Malaysia', '马达加斯加': 'Madagascar', '马尔代夫': 'Maldives',
                   '马里': 'Mali', '马耳他': 'Malta', '马绍尔群岛': 'Marshall Islands', '马提尼克岛': 'Martinique',
                   '毛里塔尼亚': 'Mauritania', '毛里求斯': 'Mauritius', '马约特': 'Mayotte', '墨西哥': 'Mexico',
                   '密克罗尼西亚': 'Micronesia', '摩尔多瓦': 'Moldova', '摩纳哥': 'Monaco', '蒙古': 'Mongolia', '黑山': 'Montenegro',
                   '蒙特塞拉特': 'Montserrat', '摩洛哥': 'Morocco', '莫桑比克': 'Mozambique', '缅甸': 'Myanmar', '纳米比亚': 'Namibia',
                   '瑙鲁': 'Nauru', '尼泊尔': 'Nepal', '荷兰': 'Netherlands', '新喀里多尼亚': 'New Caledonia', '新西兰': 'New Zealand',
                   '尼加拉瓜': 'Nicaragua', '尼日尔': 'Niger', '尼日利亚': 'Nigeria', '纽埃': 'Niue', '诺福克岛': 'Norfolk Island',
                   '挪威': 'Norway', '阿曼': 'Oman', '巴基斯坦': 'Pakistan', '帕劳': 'Palau', '巴勒斯坦': 'Palestine',
                   '巴拿马': 'Panama', '巴布亚新几内亚': 'Papua New Guinea', '巴拉圭': 'Paraguay', '秘鲁': 'Peru',
                   '菲律宾': 'Philippines', '皮特凯恩群岛': 'Pitcairn Islands', '波兰': 'Poland', '葡萄牙': 'Portugal',
                   '波多黎各': 'Puerto Rico', '卡塔尔': 'Qatar', '留尼汪岛': 'Reunion', '罗马尼亚': 'Romania', '卢旺达': 'Rwanda',
                   '俄罗斯联邦': 'Russian Federation', '圣赫勒拿': 'Saint Helena', '圣基茨和尼维斯': 'Saint Kitts-Nevis',
                   '圣卢西亚': 'Saint Lucia', '圣文森特和格林纳丁斯': 'Saint Vincent and the Grenadines', '萨尔瓦多': 'El Salvador',
                   '萨摩亚': 'Samoa', '圣马力诺': 'San Marino', '圣多美和普林西比': 'Sao Tome and Principe', '沙特阿拉伯': 'Saudi Arabia',
                   '塞内加尔': 'Senegal', '塞舌尔': 'Seychelles', '塞拉利昂': 'Sierra Leone', '新加坡': 'Singapore', '塞尔维亚': 'Serbia',
                   '斯洛伐克': 'Slovakia', '斯洛文尼亚': 'Slovenia', '所罗门群岛': 'Solomon Islands', '索马里': 'Somalia',
                   '南非': 'South Africa', '西班牙': 'Spain', '斯里兰卡': 'Sri Lanka', '苏丹': 'Sudan', '苏里南': 'Suriname',
                   '斯威士兰': 'Swaziland', '瑞典': 'Sweden', '瑞士': 'Switzerland', '叙利亚': 'Syria', '塔吉克斯坦': 'Tajikistan',
                   '坦桑尼亚': 'Tanzania', '中国台湾': 'Taiwan', '泰国': 'Thailand', '特立尼达和多巴哥': 'Trinidad and Tobago',
                   '多哥': 'Togo', '托克劳': 'Tokelau', '汤加': 'Tonga', '突尼斯': 'Tunisia', '土耳其': 'Turkey',
                   '土库曼斯坦': 'Turkmenistan', '图瓦卢': 'Tuvalu', '乌干达': 'Uganda', '乌克兰': 'Ukraine',
                   '阿拉伯联合酋长国': 'United Arab Emirates', '英国': 'United Kingdom', '美国': 'United States of America', '乌拉圭': 'Uruguay',
                   '乌兹别克斯坦': 'Uzbekistan', '瓦努阿图': 'Vanuatu', '梵蒂冈': 'Vatican City', '委内瑞拉': 'Venezuela',
                   '越南': 'Vietnam', '瓦利斯群岛和富图纳群岛': 'Wallis and Futuna', '西撒哈拉': 'Western Sahara', '也门': 'Yemen',
                   '南斯拉夫': 'Yugoslavia', '赞比亚': 'Zambia', '津巴布韦': 'Zimbabwe'}
    country = []   #国家
    year = []    #电影发兴年份
    yearnum = []  #年份数量
    mvtype = [] #电影类型
    mvtypenum  = []  #类型数量
    mvtypedata = []  #电影类型数据
    judgeScore = []  # 电影评价评分二维数组
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select score,count(score) from imdbmovie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(item[1])
    sql2 = "select country,count(country) from imdbmovie250 group by country"  #得到国家电影数目的数据
    data2 = cur.execute(sql2)
    for item in data2:
        country.append(item)
    sql3 = "select year,count(year) from imdbmovie250 group by year"  # 得到国家电影数目的数据
    data3 = cur.execute(sql3)
    for item in data2:
        year.append(item[0])
        yearnum.append(item[1])
    sql4 = "select mvtype from imdbmovie250 "  # 得到国家电影数目的数据
    data4 = cur.execute(sql4)
    for i in data4:
        data = i[0].split("|")
        for e in data:
            mvtypedata.append(e)
    mvtypedata = sorted(mvtypedata)
    for i in range(1, len(mvtypedata)):
        if mvtypedata[i] != mvtypedata[i - 1]:
            mvtype.append(mvtypedata[i])
    for mov in mvtype:
        mvtypenum.append(mvtypedata.count(mov))
    sql5 = "select score,rated from imdbmovie250 "  # 得到电影评价人数
    data5 = cur.execute(sql5)
    for item in data5:
        judgeScore.append(list(item))
    cur.close()
    conn.close()
    length  = len(mvtype)

    #豆瓣数据库载入
    Dscore = []  # 评分区间
    Dnum = []  # 评分统计数
    DcountryName = {'阿富汗': 'Afghanistan', '奥兰群岛': 'Aland Islands', '阿尔巴尼亚': 'Albania', '阿尔及利亚': 'Algeria',
                   '美属萨摩亚': 'American Samoa', '安道尔': 'Andorra', '安哥拉': 'Angola', '安圭拉': 'Anguilla',
                   '安提瓜和巴布达': 'Antigua and Barbuda', '阿根廷': 'Argentina', '亚美尼亚': 'Armenia', '阿鲁巴': 'Aruba',
                   '澳大利亚': 'Australia', '奥地利': 'Austria', '阿塞拜疆': 'Azerbaijan', '孟加拉': 'Bangladesh', '巴林': 'Bahrain',
                   '巴哈马': 'Bahamas', '巴巴多斯': 'Barbados', '白俄罗斯': 'Belarus', '比利时': 'Belgium', '伯利兹': 'Belize',
                   '贝宁': 'Benin', '百慕大': 'Bermuda', '不丹': 'Bhutan', '玻利维亚': 'Bolivia',
                   '波斯尼亚和黑塞哥维那': 'Bosnia and Herzegovina', '博茨瓦纳': 'Botswana', '布维岛': 'Bouvet Island', '巴西': 'Brazil',
                   '文莱': 'Brunei', '保加利亚': 'Bulgaria', '布基纳法索': 'Burkina Faso', '布隆迪': 'Burundi', '柬埔寨': 'Cambodia',
                   '喀麦隆': 'Cameroon', '加拿大': 'Canada', '佛得角': 'Cape Verde', '中非': 'Central African Republic',
                   '乍得': 'Chad', '智利': 'Chile', '圣诞岛': 'Christmas Islands', '科科斯（基林）群岛': 'Cocos (keeling) Islands',
                   '哥伦比亚': 'Colombia', '科摩罗': 'Comoros', '刚果（金）': 'Congo (Congo-Kinshasa)', '刚果': 'Congo',
                   '库克群岛': 'Cook Islands', '哥斯达黎加': 'Costa Rica', '科特迪瓦': 'Cote D’Ivoire', '中国大陆': 'China',
                   '克罗地亚': 'Croatia', '古巴': 'Cuba', '捷克': 'Czech', '塞浦路斯': 'Cyprus', '丹麦': 'Denmark', '吉布提': 'Djibouti',
                   '多米尼加': 'Dominica', '东帝汶': 'Timor-Leste', '厄瓜多尔': 'Ecuador', '埃及': 'Egypt',
                   '赤道几内亚': 'Equatorial Guinea', '厄立特里亚': 'Eritrea', '爱沙尼亚': 'Estonia', '埃塞俄比亚': 'Ethiopia',
                   '法罗群岛': 'Faroe Islands', '斐济': 'Fiji', '芬兰': 'Finland', '法国': 'France',
                   '法国大都会': 'Franch Metropolitan', '法属圭亚那': 'Franch Guiana', '法属波利尼西亚': 'French Polynesia',
                   '加蓬': 'Gabon', '冈比亚': 'Gambia', '格鲁吉亚': 'Georgia', '德国': 'Germany', '加纳': 'Ghana',
                   '直布罗陀': 'Gibraltar', '希腊': 'Greece', '格林纳达': 'Grenada', '瓜德罗普岛': 'Guadeloupe', '关岛': 'Guam',
                   '危地马拉': 'Guatemala', '根西岛': 'Guernsey', '几内亚比绍': 'Guinea-Bissau', '几内亚': 'Guinea', '圭亚那': 'Guyana',
                   '中国香港': 'Hong Kong', '海地': 'Haiti', '洪都拉斯': 'Honduras', '匈牙利': 'Hungary', '冰岛': 'Iceland',
                   '印度': 'India', '印度尼西亚': 'Indonesia', '伊朗': 'Iran', '伊拉克': 'Iraq', '爱尔兰': 'Ireland',
                   '马恩岛': 'Isle of Man', '以色列': 'Israel', '意大利': 'Italy', '牙买加': 'Jamaica', '日本': 'Japan',
                   '泽西岛': 'Jersey', '约旦': 'Jordan', '哈萨克斯坦': 'Kazakhstan', '肯尼亚': 'Kenya', '基里巴斯': 'Kiribati',
                   '韩国': 'South Korea', '朝鲜': 'Korea (North)', '科威特': 'Kuwait', '吉尔吉斯斯坦': 'Kyrgyzstan', '老挝': 'Laos',
                   '拉脱维亚': 'Latvia', '黎巴嫩': 'Lebanon', '莱索托': 'Lesotho', '利比里亚': 'Liberia', '利比亚': 'Libya',
                   '列支敦士登': 'Liechtenstein', '立陶宛': 'Lithuania', '卢森堡': 'Luxembourg', '中国澳门': 'Macau',
                   '马其顿': 'Macedonia', '马拉维': 'Malawi', '马来西亚': 'Malaysia', '马达加斯加': 'Madagascar', '马尔代夫': 'Maldives',
                   '马里': 'Mali', '马耳他': 'Malta', '马绍尔群岛': 'Marshall Islands', '马提尼克岛': 'Martinique',
                   '毛里塔尼亚': 'Mauritania', '毛里求斯': 'Mauritius', '马约特': 'Mayotte', '墨西哥': 'Mexico',
                   '密克罗尼西亚': 'Micronesia', '摩尔多瓦': 'Moldova', '摩纳哥': 'Monaco', '蒙古': 'Mongolia', '黑山': 'Montenegro',
                   '蒙特塞拉特': 'Montserrat', '摩洛哥': 'Morocco', '莫桑比克': 'Mozambique', '缅甸': 'Myanmar', '纳米比亚': 'Namibia',
                   '瑙鲁': 'Nauru', '尼泊尔': 'Nepal', '荷兰': 'Netherlands', '新喀里多尼亚': 'New Caledonia', '新西兰': 'New Zealand',
                   '尼加拉瓜': 'Nicaragua', '尼日尔': 'Niger', '尼日利亚': 'Nigeria', '纽埃': 'Niue', '诺福克岛': 'Norfolk Island',
                   '挪威': 'Norway', '阿曼': 'Oman', '巴基斯坦': 'Pakistan', '帕劳': 'Palau', '巴勒斯坦': 'Palestine',
                   '巴拿马': 'Panama', '巴布亚新几内亚': 'Papua New Guinea', '巴拉圭': 'Paraguay', '秘鲁': 'Peru',
                   '菲律宾': 'Philippines', '皮特凯恩群岛': 'Pitcairn Islands', '波兰': 'Poland', '葡萄牙': 'Portugal',
                   '波多黎各': 'Puerto Rico', '卡塔尔': 'Qatar', '留尼汪岛': 'Reunion', '罗马尼亚': 'Romania', '卢旺达': 'Rwanda',
                   '俄罗斯联邦': 'Russian Federation', '圣赫勒拿': 'Saint Helena', '圣基茨和尼维斯': 'Saint Kitts-Nevis',
                   '圣卢西亚': 'Saint Lucia', '圣文森特和格林纳丁斯': 'Saint Vincent and the Grenadines', '萨尔瓦多': 'El Salvador',
                   '萨摩亚': 'Samoa', '圣马力诺': 'San Marino', '圣多美和普林西比': 'Sao Tome and Principe', '沙特阿拉伯': 'Saudi Arabia',
                   '塞内加尔': 'Senegal', '塞舌尔': 'Seychelles', '塞拉利昂': 'Sierra Leone', '新加坡': 'Singapore', '塞尔维亚': 'Serbia',
                   '斯洛伐克': 'Slovakia', '斯洛文尼亚': 'Slovenia', '所罗门群岛': 'Solomon Islands', '索马里': 'Somalia',
                   '南非': 'South Africa', '西班牙': 'Spain', '斯里兰卡': 'Sri Lanka', '苏丹': 'Sudan', '苏里南': 'Suriname',
                   '斯威士兰': 'Swaziland', '瑞典': 'Sweden', '瑞士': 'Switzerland', '叙利亚': 'Syria', '塔吉克斯坦': 'Tajikistan',
                   '坦桑尼亚': 'Tanzania', '中国台湾': 'Taiwan', '泰国': 'Thailand', '特立尼达和多巴哥': 'Trinidad and Tobago',
                   '多哥': 'Togo', '托克劳': 'Tokelau', '汤加': 'Tonga', '突尼斯': 'Tunisia', '土耳其': 'Turkey',
                   '土库曼斯坦': 'Turkmenistan', '图瓦卢': 'Tuvalu', '乌干达': 'Uganda', '乌克兰': 'Ukraine',
                   '阿拉伯联合酋长国': 'United Arab Emirates', '英国': 'United Kingdom', '美国': 'United States of America',
                   '乌拉圭': 'Uruguay',
                   '乌兹别克斯坦': 'Uzbekistan', '瓦努阿图': 'Vanuatu', '梵蒂冈': 'Vatican City', '委内瑞拉': 'Venezuela',
                   '越南': 'Vietnam', '瓦利斯群岛和富图纳群岛': 'Wallis and Futuna', '西撒哈拉': 'Western Sahara', '也门': 'Yemen',
                   '南斯拉夫': 'Yugoslavia', '赞比亚': 'Zambia', '津巴布韦': 'Zimbabwe'}
    Dcountry = []  # 国家
    Dyear = []  # 电影发兴年份
    Dyearnum = []  # 年份数量
    Dmvtype = []  # 电影类型
    Dmvtypenum = []  # 类型数量
    Dmvtypedata = []  # 电影类型数据
    DjudgeScore = []  # 电影评价人数
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    Dsql = "select score,count(score) from doubanmovie250 group by score"
    Ddata = cur.execute(Dsql)
    for item in Ddata:
        Dscore.append(item[0])
        Dnum.append(item[1])
    Dsql2 = "select country,count(country) from doubanmovie250 group by country"  # 得到国家电影数目的数据
    Ddata2 = cur.execute(Dsql2)
    for item in Ddata2:
        Dcountry.append(item)
    Dsql3 = "select year,count(year) from doubanmovie250 group by year"  # 得到国家电影数目的数据
    Ddata3 = cur.execute(Dsql3)
    for item in Ddata2:
        Dyear.append(item[0])
        Dyearnum.append(item[1])
    Dsql4 = "select mvtype from doubanmovie250 "  # 得到国家电影数目的数据
    Ddata4 = cur.execute(Dsql4)
    for i in Ddata4:
        data = i[0].split("|")
        for e in data:
            Dmvtypedata.append(e)
    Dmvtypedata = sorted(Dmvtypedata)
    for i in range(1, len(Dmvtypedata)):
        if Dmvtypedata[i] != Dmvtypedata[i - 1]:
            Dmvtype.append(Dmvtypedata[i])
    for mov in Dmvtype:
        Dmvtypenum.append(Dmvtypedata.count(mov))
    Dsql5 = "select score,rated from doubanmovie250 "  # 得到电影评价人数
    Ddata5 = cur.execute(Dsql5)
    for item in Ddata5:
        DjudgeScore.append(list(item))
    cur.close()
    conn.close()
    Dlength = len(Dmvtype)





    # scorecompare 国家矩阵图的数据处理---处理国家名 将imdb 与 豆瓣 的数据扩充至并集数据

    countryList = []  # 存储imdb并集 的电影国名数据
    DcountryList = []  # 存储豆瓣的并集电影国名数据
    countryUnio = []  # 存储电影国名并集
    countryNum = []  # 存储豆瓣的电影数量数据
    DcountryNum = []  # 存储imdb的电影数量数据
    for i in range(0, len(country)):
        countryList.append(country[i][0])  # imdb 电影国家列表
    for i in range(0, len(Dcountry)):
        DcountryList.append(Dcountry[i][0])  # 豆瓣电影国家列表
    countryUnio = list(set(countryList).union(set(DcountryList)))  # 豆瓣和imdb电影国家并集

    for i in range(0, len(countryUnio)):
        countryNum.append(0)
        DcountryNum.append(0)
    for i in range(0, len(countryUnio)):
        for j in range(0, len(country)):
            if countryUnio[i] == country[j][0]:
                countryNum[i] = country[j][1]


    for i in range(0, len(countryUnio)):
        for j in range(0, len(Dcountry)):
            if countryUnio[i] == Dcountry[j][0]:
                DcountryNum[i] = Dcountry[j][1]



    return  render_template("scorecompare.html",score = score,num = num,country = country,countryName = countryName,year =year,yearnum = yearnum,mvtypenum = mvtypenum,mvtype = mvtype,length = length,Dscore = Dscore,Dnum = Dnum,Dcountry = Dcountry,DcountryName = DcountryName,Dyear =Dyear,Dyearnum = Dyearnum,Dmvtypenum = Dmvtypenum,Dmvtype = Dmvtype,Dlength = Dlength,countryUnio = countryUnio,countryNum = countryNum,DcountryNum = DcountryNum,judgeScore = judgeScore,DjudgeScore = DjudgeScore)

#词云
@app.route('/word')
def word():
    return  render_template("word.html")



#得到电影数据
countryUnio = ['德国', '意大利', '英国', '西班牙', '韩国', '印度', '新西兰', '黎巴嫩', '中国香港', '墨西哥', '巴西', '爱尔兰', '阿根廷', '丹麦', '泰国', '中国大陆', '美国', '伊朗', '澳大利亚', '瑞典', '日本', '法国', '中国台湾', '加拿大']
movies = []
conn = sqlite3.connect("movie.db")
cur = conn.cursor()
sql = "select * from doubanmovie250 "
data = cur.execute(sql)
for item in data:
    data = []
    for item2 in item:
        data.append(item2)
    movies.append(data)
cur.close()
conn.close()

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
userNum = len(users)+1
# 生成随机数组
def initRandomMovs():
    randomNums = []
    while 1:
        i = random.randint(0, 250)
        randomNums.append(i)
        if len(set(randomNums)) == 6:
            break

    randomMovs = []  # 存储随机生成的电影
    for i in randomNums:
        randomMovs.append(movies[i - 1])
    return randomMovs

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
    if len(similarUsers) == 0:
        similarUsers.append("wu")
        return similarUsers
    #对得到的原始数据进行排序
    similarUsers = sorted(similarUsers, key=functools.cmp_to_key(compare_personal), reverse=False)
    # 参观者没看过而最相似用户看过的电影 差集
    viewerMovSee = list(set(dict(users[similarUsers[0][0]-1][1]).keys()).difference(set(similarUsers[0][1])))
    similarUsers[0].append(viewerMovSee)
    return similarUsers[0]

viewer = []
chooses = []
viewer.append(userNum)
similarlestUser = []
#电影推荐
@app.route('/recommov',methods = ['GET','POST'])
def recommov():

    randomMovs = initRandomMovs()
    if request.method == 'GET':  # 无表格提交

        return render_template("recommov.html", randomMovs=randomMovs, viewer=viewer,similarlestUser = similarlestUser)
    else:

        # 有表格提交
        # 删除上次提交的数据
        choose0 = []
        choose1 = []
        choose2 = []
        choose3 = []
        choose4 = []
        choose5 = []

        if len(chooses)>=20:
            while(len(chooses)!=0):
                chooses.pop()
        if len(viewer) !=1:
            viewer.pop()
        # 读取数据
        text = request.form.get('mov0')
        textrat = request.form.get('mov0rat')
        if text != None:
            choose0.append(int(text))
            choose0.append(float(textrat))
            chooses.append(choose0)
        text = request.form.get('mov1')
        textrat = request.form.get('mov1rat')
        if text != None:
            choose1.append(int(text))
            choose1.append(float(textrat))
            chooses.append(choose1)
        text = request.form.get('mov2')
        textrat = request.form.get('mov2rat')
        if text != None:
            choose2.append(int(text))
            choose2.append(float(textrat))
            chooses.append(choose2)
        text = request.form.get('mov3')
        textrat = request.form.get('mov3rat')
        if text != None:
            choose3.append(int(text))
            choose3.append(float(textrat))
            chooses.append(choose3)
        text = request.form.get('mov4')
        textrat = request.form.get('mov4rat')
        if text != None:
            choose4.append(int(text))
            choose4.append(float(textrat))
            chooses.append(choose4)
        text = request.form.get('mov5')
        textrat = request.form.get('mov5rat')
        if text != None:
            choose5.append(int(text))
            choose5.append(float(textrat))
            chooses.append(choose5)


        viewer.append(chooses)
        #找到最相似喜好的用户
        similarlestUsertem = get_similarUsers()
        if len(similarlestUser) !=0:
            similarlestUser.pop()
        similarlestUser.append(similarlestUsertem)
        return redirect(url_for('recommov'))
    return render_template("recommovR.html",viewer=viewer, similarlestUser=similarlestUser)





#电影推荐出数据展示
@app.route('/recommovR')
def recommovR():
    if len(users) < viewer[0]:
        saveViewer()

    return  render_template("recommovR.html",similarlestUser=similarlestUser,movies =movies)

def saveViewer():
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    strmov = ''
    for movie in viewer[1]:
        strmov = strmov + '|' + str(movie[0]) + ',' + str(int(movie[1]))
    strmov = "'" + strmov + "'"
    print(strmov)
    sql4 = 'insert into userData(id,userMov_Id_Rate) values (%d,%s)' % (viewer[0], strmov)
    cur.execute(sql4)
    conn.commit()
    cur.close()
    conn.close()

#留言板
@app.route('/messageCenter',methods = ['GET','POST'])
def messageCenter():

    if request.method == 'GET':                 #无表格提交
        conn = sqlite3.connect('message.db')
        cur = conn.cursor()
        data2 =[]
        says = []
        sql2 = "select title,text,user,date from message"
        data2 = cur.execute(sql2)
        for item in data2:
            says.append({
                "title": item[0],
                "text": item[1],
                "user": item[2],
                "date": item[3]
            })

        cur.close()
        conn.close()
        return render_template("messageCenter.html",says = says)
    else:                                        #有表格提交
        conn = sqlite3.connect('message.db')
        cur = conn.cursor()
        data = []
        title = request.form.get('say_title')
        data.append("'"+title+"'")
        text = request.form.get('say')
        data.append("'" + text + "'")
        user = request.form.get('say_user')
        data.append("'" + user+ "'")
        date= time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        data.append("'" + date + "'")
        sql = '''
                       insert into message (title,text,user,date)
                       values(%s)'''%",".join(data)


        cur.execute(sql)
        conn.commit()

        return redirect(url_for('messageCenter'))




if __name__ == '__main__':
    app.run(debug=True)
