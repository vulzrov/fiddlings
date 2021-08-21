import sqlite3
import urllib.request as request
import urllib.error
import ssl
import twurl
import json

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

#表Users。用作栈以及用户集合。

cur.execute('''
            CREATE TABLE IF NOT EXISTS Users
            (id INTEGER PRIMARY KEY, name TEXT UNIQUE, retrieved INTEGER)
            ''')

#一、几个关键词的意义

  #1. PRIMARY KEY
    # Automatically adds the key value for any row we insert into a table using a special type of data column.
    # Navicate牛逼的地方：可以自定义key的赋值算法。

  #2. UNIQUE（加在列的数据类型后时）
    # Indicate that we'll not allow SQLite insert 2 rows with same value for name.

#二、表的设计思路

  #1. 考虑所需功能
    # Users表即需要作为集合储存所有账户的信息，也需要在循环中被当作栈使用。

  #2. 决定列和列的数据类型
    # Users表显然需要两个列，name存储用户名，retrived存储“是否被处理过”。
    # SQLite没有bool类，所以retrived用数字1/0表示。

  #3. 根据需求修改
    # Relations要表示账号之间的follow关系。
    # 考虑到字符串占用的内存远大于数字，我们给每个账户赋一个id，而不是直接用用户名对应账户。
    # 于是有了第三个列，id INTEGER PRIMARY KEY

#表Relations。用于存储用户之间的关系。
cur.execute('''
            CREATE TABLE IF NOT EXISTS Relations
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))
            ''')
# 关键词 UNIQUE(列1，列2，...) (独立一列)
  # Indicate that we'll not allow SQLite insert 2 rows with same value for tuple (列1，列2，...).

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    Twitter_user_account = input('输入推特用户名，或输入“quit”退出：')
    if Twitter_user_account == 'quit': #输入了quit，退出程序
        break
    if len(Twitter_user_account) < 1: #没有输入用户名，从栈中取一个未被操作过的账户
        try:
            cur.execute('''
                SELECT id,name FROM Users WHERE retrieved = 0 LIMIT 1
                        ''')
            from_id,Twitter_user_account = cur.fetchone()
        except:
            print('No unretrieved Twitter account in Table "Users"!')
            continue
    else: #输入了用户名
        cur.execute('''
            SELECT id FROM Users WHERE name=? LIMIT 1
                    ''',(Twitter_user_account,))
        try: #输入的推特用户名已经在数据库中
            from_id = cur.fetchone()[0]
        except: #输入的推特用户名不在数据库中，要添加。
            cur.execute('''
                INSERT OR IGNORE INTO Users (name,retrieved) VALUES (?,0)
                        ''',(Twitter_user_account,))
            conn.commit()
            if cur.rowcount != 1: # cur.rowcount返回cur发生变化的行的数量
                print('Error inserting account:',Twitter_user_account)
                continue
            from_id = cur.lastrowid # cur.lastrowid返回最后发生变化的行的primary_id


    url = twurl.augment(TWITTER_URL,{'screen_name': Twitter_user_account, 'count':'20'})
    print('Retrieving',url)

    try:
        connection = request.urlopen(url, context = ctx)
    except Exception as err: #无法连接到推特api，或无法在推特找到这个账户的信息
        print('Failed to Retrieve',err)
        break

    data = connection.read().decode()
    headers = dict(connection.getheaders())

    print('Remaining',headers['x-rate-limit-remaining'])
    # Rate Limit 访问速率限制
      # Every day many thousands of developers make requests to the Twitter API. 
      # To help manage the sheer volume of these requests, limits are placed on the number of requests that can be made. 
      # These limits help us provide the reliable and scalable API that our developer community relies on. 

      # The maximum number of requests that are allowed is based on a time interval, some specified period or window of time. 
        # （window of time：时间段）
      # The most common request limit interval is fifteen minutes. 
      # If an endpoint has a rate limit of 900 requests/15-minutes, then up to 900 requests over any 15-minute interval is allowed. 

      # 本例中，followers look up 的速率限制是 15 requests/15-minutes。
      # headers中‘x-rate-limit-remaining’对应的值为“本时间段内剩余的访问次数”。


    #检查收到的json回复是否正常
    try:
        js = json.loads(data)
    except:
        print('Unable to parse json')
        print(data)
        break
    if 'users' not in js:
        print('Incorrect JSON received')
        print(json.dumps(js,indent=4))
        continue

    #在Users库中将刚刚处理的账户标记为“已处理”
    cur.execute('''
        UPDATE Users SET retrieved=1 WHERE name=? 
                ''', (Twitter_user_account,))

    for u in js['users']:
        friend = u['screen_name']
        cur.execute('''
            SELECT id FROM Users WHERE name=? LIMIT 1
                    ''',(friend,))
        try: # friend在库里
            to_id = cur.fetchone()[0]
        except: # friend不在库里
            cur.execute('''
                INSERT OR IGNORE INTO Users (name,retrieved) VALUES (?,0)
                        ''',(friend,))
            conn.commit()
            if cur.rowcount != 1 :
                print('Error inserting account:',friend)
                continue
            to_id = cur.lastrowid
        cur.execute('''
            INSERT OR IGNORE INTO Relations (from_id, to_id) VALUES (?,?)
                    ''',(from_id, to_id))
        conn.commit()
    conn.commit()



cur.close()