# -*- coding = utf-8 -*-
# @Time: 2022/3/9 15:37
# @Author: mk310
# @File: test.re.py
# @Software:PyCharm

# 正则表达式 模式串匹配

import re
pat = re.compile("aa")  #匹配的模式窜
e = pat.search("abddaad") #被匹配的字符串
print(e)
print(re.findall("a","aafefefes")) #前面的是模式串 后面匹配的串

# sub

print(re.sub("a","hu","feufhuehfueaaaaaaaa")) #将a 替换成hu
