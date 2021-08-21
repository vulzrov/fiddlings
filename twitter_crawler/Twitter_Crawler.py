from urllib.request import urlopen
import urllib.error
import twurl
import json
import sqlite3
import ssl

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Twitter 
            (name TEXT, retrieved INTEGER, friends INTEGER)''')
#用户名  |  判断条件“该用户是否已被处理过” |  受欢迎程度（在多少个已被处理的用户好友名单中出现）

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
#ssl的意义是安全认证。
#ssl context是密码，protocol（协议），certification（证书），TLS选项，TLS扩展的集合。
#由于具有相同设置的多个连接很常见，因此将他们放在context中。创建新连接时，只要引用context即可，极大减少了工作量。

while True:
    acct = input('Enter a Twitter account, or quit: ')
    if (acct == 'quit'): 
        break
    if (len(acct) < 1):
        cur.execute('SELECT name FROM Twitter WHERE retrieved = 0 LIMIT 1')
        #取一行没有被处理过的用户数据（LIMIT 1）
        try:
            acct = cur.fetchone()[0]
            #fetchone()方法取SELECT语句返回的所有行中的第一行，以tuple形式返回所有元素组成的序列。
            #这里是取'name'这一项。
        except:
            print('No unretrieved Twitter accounts found.')
            continue

    url = twurl.augment(TWITTER_URL,{'screen_name': acct,'count': '20'})
        #1. 过频繁的api请求导致服务器负荷过大。因此多数企业的服务器都有访问“门槛”，即url经过算法加密后才能访问。
          #twitter不例外。twurl封装了twitter的加密算法。
          #这里是生成了访问账号好友列表所需的url，并设定一次提取好友列表中的20人。
        #2. 注意： To make authorized calls to Twitter’s APIs, you must first obtain an OAuth access token as described in the Textbook.
          #按 https://developer.twitter.com/en/docs/basics/authentication/guides/authorizing-a-request 
          #描述的流程，获取"consumer_key","consumer_secret","token_key","token_secret"四个参数，然后写入hidden.py文件。
        #3. API key:             2KtjQLjOIew1yTvIXaY2R3zcG
           #API secret key:      mAwSnueEK6S0eIGIsbnNkuwJJIVQOZFb1fUnmA2Sfrzt9y4SdB
           #Bearer Token:        AAAAAAAAAAAAAAAAAAAAADySSwEAAAAAgmhiI699FSTPXw0LywEPK%2FpoI%2BA%3DWnhS6H9903szLxnwqFpm0a44H45TXDN9VE1MQSeOmVIBPS6qpE
           #Access Token:        1428920541822394373-D4ZwgzNXPGWRQCdcCs0rBz2rBzw0gA
           #Access Token Secret: apBRr7j0PYkEmfhayPGSvwcqG2GHvi0kr25R28hVZZGII

    print('Retrieving',url)
    connection = urlopen(url, context = ctx)
    data = connection.read().decode()         #获取content
    headers = dict(connection.getheaders())   #获取headers，并convert to dictionary

    print('Remaining', headers['x-rate-limit-remaining'])
    js = json.loads(data)

        #以上已经完成了一个账号的好友列表提取，我们在数据库中将其标记为“已处理”。
    cur.execute('UPDATE Twitter SET retrieved=1 WHERE name = ?',(acct,))
        
    countnew = 0 #这次提取的用户列表中，之前未被提取过的用户数
    countold = 0 #这次提取的用户列表中，之前已经被提取过的用户数
    for u in js['users']:
        friend = u['screen_name']
        print(friend)
        cur.execute('SELECT friends FROM Twitter WHERE name=? LIMIT 1',(friend,))
        try:
            count = cur.fetchone()[0]
            cur.execute('UPDATE Twitter SET friends = ? WHERE name = ?',(count+1,friend))
            countold+=1
        except:
            cur.execute('''
                    INSERT INTO Twitter (name, retrieved, friends)
                    VALUES (?, 0, 1)
                        ''',(friend,))
            countnew+=1
    print('New accounts=', countnew,' Revisited=', countold)
    conn.commit()

cur.close()




