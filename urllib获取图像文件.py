#使用urllib模块获取图像文件。其他二进制文件同理。

import urllib.request, urllib.parse, urllib.error

img = urllib.request.urlopen('http://data.pr4e.org/cover3.jpg')

with open('cover3.jpg','wb') as cf:
    while True:
        data = img.read(10000)
        #为什么要加“一次读10000个字节”这个限定？
        #因为图像文件用read转化成字符串会极度膨胀，甚至会填满电脑内存，必须分批处理。
        if len(data) < 1:
            break
        cf.write(data)




