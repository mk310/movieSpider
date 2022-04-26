# -*- coding = utf-8 -*-
# @Time: 2022/3/14 20:45
# @Author: mk310
# @File: testCloud.py
# @Software:PyCharm
#生成词云

import jieba                            #分词
from matplotlib import  pyplot as plt   #绘图
from wordcloud import  WordCloud        #词云
from PIL import Image                   #图片处理
import numpy as np                      #举证运算
import sqlite3

conn = sqlite3.connect('movie.db')
cur = conn.cursor()
sql = 'select cname from doubanmovie250'
data = cur.execute(sql)

text = ""
for item in data:
    text = text + item[0]
print(text)
cur.close()
conn.close()            #获取一个超长的文本

cut = jieba.cut(text)   #剪切
string = ' '.join(cut)
print(string)

stopwords = set('')
stopwords.update(['的','来','脸','之'])
img = Image.open(r'.\static\assets\images\brain.png')          #打开图片
img_array = np.array(img)                                   #图片数组化
wc = WordCloud(
    background_color = 'white',
    mask =None,
    font_path="simkai.ttf",                                  #本机电脑字体位置C:\Windows\Fonts
    max_words=150,
    scale=1.5,
    margin=0,
    mode="RGB",
    stopwords=stopwords,
    height=500,
    width=500,
    
)
wc.generate_from_text(string)               #导入词

#绘制图片
fig = plt.figure(1)
plt.imshow(wc)                                              #按wc规则显示图片
plt.axis('off')                                             #是否显示坐标轴
# plt.show() #显示生成的词云图片
plt.savefig(r'.\static\assets\images\word.png',dpi=1000)