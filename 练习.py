import socket

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Create socket object.
  #1. 第一个参数表示地址（和协议）簇。( 指定.connect()方法的参数使用何种格式表示服务器地址 )
    # (1) socket.AF_INET：
      # 一对 (host, port) 被用于 AF_INET 地址族，
      # host 是一个表示为互联网域名表示法之内的主机名或者一个 IPv4 地址的字符串，例如 'daring.cwi.nl' 或 '100.50.200.5'，
      # port 是一个整数。
    # (2) socket.AF_UNIX：
      # 一个绑定在文件系统节点上的 AF_UNIX socket 的地址表示为一个字符串
    # (3) socket.AF_INET6：
      # 使用一个四元组 (host, port, flowinfo, scope_id)，
      # 其中 flowinfo 和 scope_id 代表了 C 库 struct sockaddr_in6 中的 sin6_flowinfo 和 sin6_scope_id 成员。
      # 对于 socket 模块中的方法， flowinfo 和 scope_id 可以被省略，只为了向后兼容。
  #2. 第二个参数表示套接字类型。
    # 一般只有 socket.SOCK_STREAM 和 socket.SOCK_DGRAM 可用

mysock.connect(('data.pr4e.org', 80))       
# Connect socket to server 'data.pr4e.org' on port 80
  # 细节：the parameter of the method is a 2-tuple.

cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode() 
# Write your command in proper HTTP format, and encode it into 'bytes' type.
  # About the format.
    #(1) GET + [space] + <url> + [space] + HTTP/1.0 + \r\n\r\n
    #(2) \r\n is the official 'EOL'(end of line) symbol stipulated by HTTP protocol.
      #So 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n' is a complete line, 
      #then '\r\n' means it is followed by an empty line.
      #GET request 后要跟一个空行是HTTP规定。
    #(3) 补充：
      # '\r'：光标移到行首
      # '\b'：光标左移一位
      # '\r\n'：换行。HTTP中特别规定为行终止符。
      # '\n'：换行 
      

mysock.send(cmd) 
# Send the command to socket
  # 细节：参数为‘bytes’类型。

while True:
    data = mysock.recv(512)
    # Receive data in 512-character chunks.（chunks不是术语。用字面意思‘块’理解）
      #1. socket_obj.recv(m) 参数m的含义是：m个字符对应的（对应方法可以是ASCII/UTF/...）二进制数据。
        #换句话说，m的单位是‘一个character所需的字节（bytes）数’，对UTF-8而言就是1到4浮动。
      #2. 512这个值对本例而言不重要。改成1都可以。
    if len(data) < 1:
        break
    print(data.decode(),end='')

mysock.close()


# 完整输出：
# HTTP/1.1 200 OK
# Date: Tue, 17 Aug 2021 07:36:50 GMT
# Server: Apache/2.4.18 (Ubuntu)
# Last-Modified: Sat, 13 May 2017 11:22:22 GMT
# ETag: "a7-54f6609245537"
# Accept-Ranges: bytes
# Content-Length: 167
# Cache-Control: max-age=0, no-cache, no-store, must-revalidate
# Pragma: no-cache
# Expires: Wed, 11 Jan 1984 05:00:00 GMT
# Connection: close
# Content-Type: text/plain （指明了文件类型，为纯文本文件）
  #以上是'Headers'

# But soft what light through yonder window breaks
# It is the east and Juliet is the sun
# Arise fair sun and kill the envious moon
# Who is already sick and pale with grief
  #以上为文件‘romeo.txt’中的实际内容。