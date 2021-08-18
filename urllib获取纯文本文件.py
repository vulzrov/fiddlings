#使用urllib模块获取纯文本文件，并统计单词出现次数

import urllib.request,urllib.parse,urllib.error

count = dict()
f = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
# 1. 实际运转原理与socket相同，隐藏了细节让开发更简单。
# 2. 将f视为file_obj即可。注意f内含二进制数据即‘bytes’类型，而file_obj含'str'类型数据。
# 3. f去掉了header部分。
# 4. f不用close()。
for line in f:
    words = line.decode().strip().split()
    for word in words:
        count[word] = count.get(word,0) + 1

print(count)
