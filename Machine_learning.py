import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn                           #简化编程
import torch.nn.functional as F
from torchvision import datasets, transforms

#构建模型
class Model_Logistic_Regression(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
        self.lin = nn.Linear(28*28,10)

    def forward(self,x):
        return self.lin(x)
    #forward方法对 nn.Module 对象非常重要。

    #从类的__call__()方法讲起。
      #Python中类的实例（对象）可以被当做函数对待。而为了将一个类实例当做函数调用，我们需要在类中实现__call__()方法。
      #__call__()方法接受一定数量的变量作为输入。
      #假设x是X类的一个实例。那么调用x.__call__(1,2)等同于调用x(1,2)。实例本身在这里相当于一个函数。
    # nn.Module 对象的__call__()方法使用forward方法来计算返回值。
      #我们可以简单理解成：nn.Module 对象的__call__方法就是forward方法。尽管事实上要复杂得多。

    #再讲讲本例.__init__()中出现的 nn.Linear 对象。
      # nn.Linear 对象是pytorch内置的nn.Module对象的一个子类。
      #其含义为“Linear transform”。y(返回值/输出)=torch.matmul(x(输入),W)+b
      #实现该对象实际上不难，可以尝试。


train_set = datasets.MNIST('./datasets', train = True, transform = transforms.ToTensor(), download = True)
test_set = datasets.MNIST('./datasets', train = False, transform = transforms.ToTensor(), download = True)

train_loader = torch.utils.data.DataLoader(train_set,batch_size=100,shuffle=True)
test_loader = torch.utils.data.DataLoader(test_set,batch_size=100,shuffle=False)



#初始化
  #调用模型（生成一个模型类的实例）
model = Model_Logistic_Regression()

  #生成评估器（指定计算loss的算法）
criterion = nn.CrossEntropyLoss()
    #交叉熵算法
    #nn.CrossEntropyLoss()也是一个nn.Module子类。

  #生成操作器
optimizer = torch.optim.SGD(model.parameters(),lr=0.1)
    #model.parameters()方法返回模型的所有参数


#训练
for images, labels in train_loader:

    #清零optimizer的gradient缓冲区
    optimizer.zero_grad()

    #forward pass
      #图像扁平化（生成模型可处理的x）。本例中将图像矩阵转化为向量。
    x = images.view(-1,28*28)
      #将x传递给模型
    y = model(x)
      #求出loss
    loss = criterion(y,labels)

    #backward pass
    loss.backward()
    optimizer.step()


#测试
correct = 0
total = len(test_set)
with torch.no_grad():
    for images, labels in test_loader:
        x = images.view(-1,28*28)
        y = model(x)
        predictions = torch.argmax(y,dim=1)
        correct += torch.sum((predictions == labels).float())

accuracy = correct/total
print('test accuracy: {}'.format(accuracy))


#可视化
W,b = model.parameters()

fig, ax = plt.subplots(1,10,figsize=(20,2))
for digit in range(10):
    ax[digit].imshow(W[digit,:].detach().view(28,28),cmap='gray')

plt.show()