import numpy as np                              #矩阵处理模块
import matplotlib.pyplot as plt                 #可视化模块（面向过程）
import torch                                    #pytorch主框架
import torch.nn.functional as F                 #简化编程过程
from torchvision import datasets, transforms    #数据获取与转化模块


#数据下载与提取
train_set = datasets.MNIST('./datasets',train = True, transform = transforms.ToTensor(), download= True)
test_set = datasets.MNIST('./datasets',train = False, transform = transforms.ToTensor(), download= True)

#数据重整与分批
train_loader = torch.utils.data.DataLoader(train_set, batch_size = 100, shuffle = True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size = 100, shuffle = False)

#初始化参数和操作器
W = torch.randn(28*28, 10)/np.sqrt(28*28)
W.requires_grad_()
b = torch.zeros(10, requires_grad = True)#需要训练的参数，把requires_grad参数设成True（vector）或用.requires_grad_()方法（Matrix）。
optimizer = torch.optim.SGD([W,b],lr = 0.1)#指定学习算法，需学习的参数，跨步大小   

#训练循环（学习）
for images,labels in train_loader:
    #清空gradient缓冲区
    optimizer.zero_grad()
    #执行forward pass
        #图像扁平化
    x = images.view(-1, 28*28)
        #计算loss值
            #计算矩阵y
    y = torch.matmul(x,W) + b
            #计算loss
    loss = F.cross_entropy(y, labels)
    #执行backward pass
        #计算gradient并将其累加到缓冲区
    loss.backward()
        #更新参数
    optimizer.step()

#测试结果
correct = 0
total = len(test_set)#小注意：正确率=正确判断图片数/总图片数，但具体过程中我们还是用批处理。
with torch.no_grad():
#W和b的requires_grad_被指定为是，但测试和使用时不更新它们，也用不到gradient值，白白浪费计算量。因此在测试块内将该参数指定为否。
    for images, labels in test_loader:

        x = images.view(-1,28*28)       #扁平化图像

        y = torch.matmul(x, W) + b      #计算y矩阵

        predictions = torch.argmax(y, dim = 1)
        #先讲下y矩阵是什么。
        #y为 100 * 10 矩阵。我们将数据分成批，100 个（image,label）组为一批。我们要辨认数字0-9。
        #y的每一行对应批次中的一个图像，每行的元素“并不是但正相关了”这个图像是0/1/2/.../9的概率。
        #关于.argmax()函数，参阅笔记。

        correct += torch.sum((predictions == labels).float())
        #predictions不难理解是一个长度为100的向量。labels也是长度为100的向量。
        #argmax返回index，因此和labels一样predictions的元素是数字0/1/2/.../9。
        #实际上predictions就是模型对每张图的识别结果。
        #(predictions == labels)将predictions和labels的每个元素比较，生成一个bool张量。
        #.float()将这个张量的元素转为浮点类型。0：错误，1：正确。

accuracy = correct/total
print('Test accuracy: {}'.format(accuracy))


#可视化filter
 #建框架。fig是图像本体，ax为轴。子图向轴中填充。figsize参数为比例缩放。
fig, ax = plt.subplots(1,10,figsize=(20,2))

for digit in range(10):
    ax[digit].imshow(W[:,digit].detach().view(28,28),cmap='gray')
    #1.讲讲W是什么。
      #W和b是学习结果，filter信息包括W和b。出于方便考虑，我们忽略了b。因为实际应用中就不怎么可视化filter，这里只是展示、教学。
      #W是784（28*28）*10矩阵。每一列向量与扁平化后的图像相乘结果与“该图是数字0/1/2/.../9的概率”正相关（即y矩阵行向量的元素）。
    #2.讲讲.detach()方法什么作用
      #我们构建W时调用了requires_grad_()方法。应用端把它理解成“告诉解释器这个参数是要学习的”就够了。
      #但实际上这是“追踪gradient值”的意思。
      #与测试结果中一样，当我们不需要再学习这个参数时，追踪gradient就很多余。而且，这个追踪计算量巨大。我们必须停止追踪。
      #.detach()方法让W的requires_grad_()永久为否。

plt.show()