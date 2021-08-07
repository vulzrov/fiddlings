import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms

class SelfDefined_ReLU(nn.Module):
    def __init__(self,dim_in,dim_out):
        nn.Module.__init__(self)
        self.W = nn.Parameter(torch.randn(dim_in,dim_out)/np.sqrt(dim_in))
        self.W.requires_grad_()
        self.b = nn.Parameter(torch.zeros(dim_out,requires_grad = True))

    #讲讲parameter与buffer：pytorch模型的两种参数。 
    #pytorch"模型"，即 nn.Module 的子类，有两种参数。
      #parameter参数为backward后需要更新的参数。buffer参数在backward后不更新。
      #通过 model.parameters() 和 model.buffers() 方法来返回模型的这两类参数。

      #parameter参数有两种创建方法：
        #1. 将成员变量（self.xxxx）通过nn.Parameter()创建。如我们在 SelfDefined_ReLU 中书写的。
        #2. 若没有添加成员变量，用nn.Parameter()创建的是一个普通 nn.Parameter 对象，则要将该
        #变量通过register_parameter()注册。
        #syntax: self.register_parameter('param变量名',<param对象>)

      #buffer参数创建方法：
        #创建tensor, 再将tensor传递给register_buffer()来完成注册。（与parameter创建方法二相同）
        #syntax: self.register_buffer('buffer变量名',<tensor对象>)

    def forward(self,x):
        z = F.relu(x)
        return torch.matmul(z,self.W)+self.b


class Model_MLP(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
        self.layer1_linear = nn.Linear(28*28,500)
        self.layer2_ReLU = SelfDefined_ReLU(500,10)

    def forward(self,x):
        hidden_z = self.layer1_linear(x)
        return self.layer2_ReLU(hidden_z)


#preparing data
mnist_train = datasets.MNIST('./datasets',train = True, transform = transforms.ToTensor(),download = True)
mnist_test = datasets.MNIST('./datasets',train = False, transform = transforms.ToTensor(),download = True)

train_loader = torch.utils.data.DataLoader(mnist_train, batch_size = 100, shuffle = True)
test_loader = torch.utils.data.DataLoader(mnist_test, batch_size = 100, shuffle = False)

#initialize
model = Model_MLP()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(),lr = 0.7)

#train
for epoch in range(3):
    for images, labels in train_loader:
        optimizer.zero_grad()
        x = images.view(-1,28*28)
        y = model(x)
        loss = criterion(y, labels)

        loss.backward()
        optimizer.step()

#test
correct = 0
total = len(mnist_test)
with torch.no_grad():
    for images, labels in test_loader:
        optimizer.zero_grad()
        x = images.view(-1,28*28)
        y = model(x)
        predictions = torch.argmax(y, dim = 1)
        correct+=torch.sum((predictions==labels).float())

accuracy  =correct/total
print('test accuracy: {}'.format(accuracy))

for param in model.parameters():
    print('parameter: {}'.format(param.shape))

