# -*- coding = utf-8 -*-
# @Time: 2022/3/11 13:36
# @Author: mk310
# @File: testXwlt.py
# @Software:PyCharm

import xlwt

workbook = xlwt.Workbook(encoding = "utf-8")
worksheet = workbook.add_sheet('sheet1') #创建工作表
for i in range(1,10):
    for j in range(i,10):
        worksheet.write(i, j, "%d*%d = %d"%(i,j,i*j))  # 矩阵坐标加内容

workbook.save("student.xls")