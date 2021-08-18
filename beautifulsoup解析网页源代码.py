#beautifulsoup解析网页源代码。解析+爬取组成完整爬虫。

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://docs.python.org'
html = urllib.request.urlopen(url,context=ctx).read()
#1. ssl作用为作用类似电线漆包线。阻止socket两端传送的信息被截获。
#2. .read()以‘bytes’二进制数据形式返回HTML源代码。否则返回网页指定的Response对象，一般是json格式。
soup = BeautifulSoup(html,'html.parser')
#创建一个BeautifulSoup实例。
  #1. 第一个参数为‘bytes’类型的HTML源代码。即分析对象。
  #2. 第二个参数为分析器，parser对象。意义是封装解析HTML的算法。
    # html.parser是python3标准库包含的。也可以额外下载BeautifulSoup提供的分析器。


# 先讲讲HTML基本语法。
# 1. HTML由tags+数据+js脚本组成。
  # tag封装数据，组成超链接/视频/输入框/图片等页面元素。
  # 最基础的tag有：<h>:标题，<p>：段落，<a>：超链接等。
# 2. tag中又包含attributes。比如archor tag <a>就有 href:链接指针，

tags = soup('a')
#将‘a’、‘p’这些字符传递给Beautifulsoup对象，会返回HTML源代码中这一类tag的所有实例组成的序列。
for tag in tags:
    print(tag)
    print(tag.contents)
    #返回tag对象包裹的数据。一般是文本。
    print(tag.attrs)
    #返回tag对象所有attributes及其值，以字典形式返回。（似乎较早版本是以2-tuple list返回的）
    print(tag.get('href',None))
    # .get方法返回tag对象指定attribute的值。
    # None为默认值。如果tag对象没有指定attribute就返回指定的默认值。
    # 这个参数有默认值，默认为None。




