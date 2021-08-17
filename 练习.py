import socket
import time

mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mysock.connect(('data.pr4e.org',80))
cmd = 'GET http://data.pr4e.org/cover3.jpg HTTP/1.0\r\n\r\n'.encode()

mysock.sendall(cmd)
# send 与 sendall 的区别。
  # 1. send
    # Send a data string to the socket.  
    # Return the number of bytes sent; 
    # this may be less than len(data) if the network is busy.
  # 2. sendall
    # Send a data string to the socket.  
    # This calls send() repeatedly until all data is sent.  
    # If an error occurs, it's impossible to tell how much data has been sent.


count = 0
picture = b''

while True:
    data = mysock.recv(5120)
    if len(data) < 1:
        break
    #time.sleep(0.25)
    count += len(data)
    print(count, len(data))
    picture += data

pos = picture.find(b'\r\n\r\n')   #find()方法返回参数字符串第一位字符的序列号（index）
with open('header.txt','w') as h:
    h.write(picture[:pos].decode())

with open('stuff.jpg','wb') as p: #'wb'向文件写入‘bytes’类型数据。'rb'类似。
    p.write(picture[pos+4:])