import wx
import os

import PIL
from PIL import Image
from PIL import ImageDraw

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets,transforms

#二值化
def binarization(image,threshold):
    result = image.convert('L')
    pixel_img = result.load()
    drawing = ImageDraw.Draw(result)
    for x in range(image.width):
        for y in range(image.height):
            if pixel_img[x,y] > threshold:
                drawing.point((x,y),fill = 255)
            else:
                drawing.point((x,y),fill = 0)
    return result

#pillow.Image对象转化为wx.Bitmap对象 
#(wxpython有pillow接口)
def PIL_to_wx(image): 
    width,height = image.size
    #依靠wx.BitmapFromBuffer函数。
    #该函数接受宽、高、pillow.Image对象，返回对应大小的wx.Bitmap对象。
    return wx.BitmapFromBuffer(width,height,image.tobytes())

#wx.Bitmap对象转化为pillow.Image对象
#（pillow无wxpython接口，wx.Bitmap需要先扁平化到字符串，再恢复为PIL.Image）
def wx_to_PIL(bitmap):
    size = tuple(bitmap.GetSize()) 
    #.GetSize()方法返回wx.Size对象，需将其转化为tuple以与PIL.Image对接。

    try:
        buf = size[0]*size[1]*3*'\x00'  #数据类型为字符串。也是扁平化图像的一种方法。
        bitmap.CopyToBuffer(buf)  #wx.Bitmap类的.CopyToBuffer方法。side effect: 更新字符串buf。

    except: #内存管理。        
        del buf
        buf = bitmap.ConvertToImage().GetData()
    return Image.frombuffer('RGB',size,buf,'raw','RGB') #从扁平化的buf中恢复图像到PIL.Image

class LR_Model(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
        self.lin = nn.Linear(28*28,10)

    def forward(self,x):
        return self.lin(x)

class SelfDefineReLU(nn.Module):
    def __init__(self,dim_in,dim_out):
        nn.Module.__init__(self)
        self.W = nn.Parameter(torch.randn(dim_in,dim_out)/np.sqrt(dim_in))
        self.W.requires_grad_()
        self.b =  nn.Parameter(torch.zeros(dim_out,requires_grad = True))

    def forward(self,x):
        z = F.relu(x)
        return torch.matmul(z,self.W)+self.b

class MLP_Model(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
        self.layer1_lin = nn.Linear(28*28,500)
        self.layer2_ReLU = SelfDefineReLU(500,10)

    def forward(self,x):
        z = self.layer1_lin(x)
        return self.layer2_ReLU(z)

class MainFrame(wx.Frame):
    def __init__(self,parent,title = '图像识别',size = (320,460)):
        wx.Frame.__init__(self,parent,title = title, size = size)
        #状态栏
        self.CreateStatusBar()
        #菜单栏
        StartMenu = wx.Menu()

        About = wx.MenuItem(StartMenu,-1,'关于应用\tCtrl+A','点击或按快捷键Ctrl+A获取应用使用说明')
        StartMenu.Append(About)
        self.Bind(wx.EVT_MENU,self.OnAbout,About)

          #关于SubMenu
        Models = wx.Menu()
        LR = wx.MenuItem(Models,-1,'Logistic Regression')
        Models.Append(LR)
        self.Bind(wx.EVT_MENU,self.OnModelsLR,LR)
        MLP = wx.MenuItem(Models,-1,'Multilayer Perceptron')
        Models.Append(MLP)
        self.Bind(wx.EVT_MENU,self.OnModelsMLP,MLP)
        StartMenu.Append(-1,'选取模型',Models)

        Navigate = wx.MenuItem(StartMenu,-1,'导航到目标文件\tCtrl+N','点击或按快捷键Ctrl+N导入图像文件')
        StartMenu.Append(Navigate)
        self.Bind(wx.EVT_MENU,self.OnNavigation,Navigate)

        Exit = wx.MenuItem(StartMenu,-1,'退出应用\tCtrl+E','点击或按快捷键Ctrl+E退出应用')
        StartMenu.Append(Exit)
        self.Bind(wx.EVT_MENU,self.OnExit,Exit)

        menubar = wx.MenuBar()
        menubar.Append(StartMenu,'开始')
        self.SetMenuBar(menubar)

        #布局
        panel = wx.Panel(self)
        VboxMain = wx.BoxSizer(wx.VERTICAL)

          #显示识别结果
        hbox1 = wx.BoxSizer()
        self.result = wx.StaticText(panel,-1,'识别结果：')
        hbox1.Add(self.result,flag = wx.ALIGN_LEFT)
        VboxMain.Add(hbox1, proportion = 0, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 20)

          #插入图像
        hbox2 = wx.BoxSizer()         
        self.image = wx.StaticBitmap(panel,-1,size = (280,280))
        hbox2.Add(self.image, proportion = 1, flag = wx.EXPAND)
        VboxMain.Add(hbox2, proportion = 1, flag = wx.LEFT|wx.RIGHT, border = 20)

        VboxMain.Add((-1,20))

          #按钮：导入图片/开始识别/退出应用。
        hbox3 = wx.BoxSizer()
        NavigateButton = wx.Button(panel,-1,'导入')
        self.Bind(wx.EVT_BUTTON,self.OnNavigation,NavigateButton)
        hbox3.Add(NavigateButton, flag = wx.RIGHT, border = 20)

        StartButton = wx.Button(panel,-1,'开始')
        hbox3.Add(StartButton,flag = wx.RIGHT, border = 20)
        self.Bind(wx.EVT_BUTTON,self.OnStartButton,StartButton)

        ExitButton = wx.Button(panel,-1,'退出')
        self.Bind(wx.EVT_BUTTON,self.OnExit,ExitButton)
        hbox3.Add(ExitButton)
        VboxMain.Add(hbox3, proportion = 0, flag = wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 20)

        panel.SetSizer(VboxMain)

    def OnAbout(self,event):
        dlg = wx.MessageDialog(self,'在菜单栏选择模型（默认为LR），点击导航或使用快捷键Ctrl+N导航到目标文件。导入文件后，按开始按钮进行识别。','说明',style = wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnModelsLR(self,event):
        train_set = datasets.MNIST('./datasets',train = True, transform = transforms.ToTensor(),download = True)

        train_loader = torch.utils.data.DataLoader(train_set, batch_size = 100, shuffle = True)

        criterion = nn.CrossEntropyLoss()
        self.model = LR_Model()
        optimizer = torch.optim.SGD(self.model.parameters(),lr = 0.1)

        for images, labels in train_loader:
            optimizer.zero_grad()
            x = images.view(-1,28*28)
            y = self.model(x)
            loss = criterion(y,labels)

            loss.backward()
            optimizer.step()

    def OnModelsMLP(self,event):
        train_set = datasets.MNIST('./datasets',train = True, transform = transforms.ToTensor(),download = True)
        train_loader = torch.utils.data.DataLoader(train_set,batch_size = 100,shuffle = True)

        self.model = MLP_Model()
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(self.model.parameters(),lr = 0.7)

        for images, labels in train_loader:
            optimizer.zero_grad()
            x = images.view(-1,28*28)
            y = self.model(x)
            loss = criterion(y,labels)
            loss.backward()
            optimizer.step()

    def OnStartButton(self,event):
        with torch.no_grad():
            x = self.Tensor1.view(28*28)
            y = self.model(x)
            self.result.SetLabel('识别结果：{}'.format(torch.argmax(y)))

    def OnNavigation(self,event):
        dlg = wx.FileDialog(self,'导入图像','','','*.*',style = wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            dir = dlg.GetDirectory()
            file = dlg.GetFilename()
            self.PIL_Image = Image.open(os.path.join(dir,file),'r').convert('RGB')
            self.PIL_Image = self.PIL_Image.resize((280,280))
            bitmap = PIL_to_wx(self.PIL_Image)
            self.image.SetBitmap(bitmap)
            bi_image = binarization(self.PIL_Image.convert('L').resize((28,28)),170)
            self.Tensor1 = transforms.ToTensor()(bi_image)

        dlg.Destroy()

    def OnExit(self,event):
        
        self.Close(True)



app = wx.App()
frame = MainFrame(None)
frame.Show()

app.MainLoop()