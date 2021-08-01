import wx
import os

def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result


class MainFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(960,530))
        self.CreateStatusBar()

        #设定菜单栏
        menu=wx.Menu()
        About=wx.MenuItem(menu,-1,'相关信息\tCtrl+A',"点击获取应用说明")
        menu.Append(About)
        Navigation=wx.MenuItem(menu,-1,'导航\tCtrl+N',"导航到目标文件。")
        menu.Append(Navigation)
        Exit=wx.MenuItem(menu,-1,'退出\tCtrl+Q',"点击退出应用。")
        menu.Append(Exit)

        menubar=wx.MenuBar()
        menubar.Append(menu,'开始')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU,self.OnAbout,About)
        self.Bind(wx.EVT_MENU,self.OnNavigation,Navigation)
        self.Bind(wx.EVT_MENU,self.OnExit,Exit)

        #设定pannel
        panel=wx.Panel(self)
        panel.SetBackgroundColour('#4f5049')

        hbox=wx.BoxSizer(wx.HORIZONTAL)
        #操作栏
        vbox1 = wx.BoxSizer(wx.VERTICAL)

        #宽
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel,label='宽:')
        hbox1.Add(st1,flag=wx.RIGHT,border=8,proportion=1)
        self.ct1 = wx.StaticText(panel,label='0')
        hbox1.Add(self.ct1,proportion=1)
        vbox1.Add(hbox1,flag=wx.EXPAND|wx.BOTTOM,border=40)

        #高
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel,label='高:')
        hbox2.Add(st2,flag=wx.RIGHT,border=8,proportion=1)
        self.ct2 = wx.StaticText(panel,label='0')
        hbox2.Add(self.ct2,proportion=1)
        vbox1.Add(hbox2,flag=wx.EXPAND|wx.BOTTOM,border=40)

        #x1坐标调整
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        ct3=wx.StaticText(panel,label='x1坐标:')
        hbox3.Add(ct3,flag=wx.RIGHT,border=8,proportion=1)
        self.sld1 = wx.Slider(panel,value=0,minValue=0,maxValue=200)
        hbox3.Add(self.sld1,flag=wx.RIGHT,border=8,proportion=0)
        self.st3 = wx.StaticText(panel,label='0')
        hbox3.Add(self.st3,proportion=1)
        vbox1.Add(hbox3,flag=wx.EXPAND|wx.BOTTOM,border=20)

        self.Bind(wx.EVT_SCROLL,self.OnSld1Scroll,self.sld1)

        #y1坐标调整
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        ct4=wx.StaticText(panel,label='y1坐标:')
        hbox4.Add(ct4,flag=wx.RIGHT,border=8,proportion=1)
        self.sld2 = wx.Slider(panel,value=0,minValue=0,maxValue=200)
        hbox4.Add(self.sld2,flag=wx.RIGHT,border=8,proportion=0)
        self.st4 = wx.StaticText(panel,label='0')
        hbox4.Add(self.st4,proportion=1)
        vbox1.Add(hbox4,flag=wx.EXPAND|wx.BOTTOM,border=20)

        self.Bind(wx.EVT_SCROLL,self.OnSld2Scroll,self.sld2)

        #x2坐标调整
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        ct5=wx.StaticText(panel,label='x2坐标:')
        hbox5.Add(ct5,flag=wx.RIGHT,border=8,proportion=1)
        self.sld3 = wx.Slider(panel,value=0,minValue=0,maxValue=200)
        hbox5.Add(self.sld3,flag=wx.RIGHT,border=8,proportion=0)
        self.st5 = wx.StaticText(panel,label='0')
        hbox5.Add(self.st5,proportion=1)
        vbox1.Add(hbox5,flag=wx.EXPAND|wx.BOTTOM,border=20)

        self.Bind(wx.EVT_SCROLL,self.OnSld3Scroll,self.sld3)

        #y2坐标调整
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        ct6=wx.StaticText(panel,label='y2坐标:')
        hbox6.Add(ct6,flag=wx.RIGHT,border=8,proportion=1)
        self.sld4 = wx.Slider(panel,value=0,minValue=0,maxValue=200)
        hbox6.Add(self.sld4,flag=wx.RIGHT,border=8,proportion=0)
        self.st6 = wx.StaticText(panel,label='0')
        hbox6.Add(self.st6,proportion=1)
        vbox1.Add(hbox6,flag=wx.EXPAND|wx.BOTTOM,border=20)

        self.Bind(wx.EVT_SCROLL,self.OnSld4Scroll,self.sld4)

        hbox.Add(vbox1,flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM,border=20)

        #操作栏与显示栏之间的分隔
        hbox.Add((20,-1))

        #图片显示栏
        self.path='source/__A2.png'

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.orimap=wx.Bitmap(self.path)
        bitmap=scale_bitmap(self.orimap,800,450)
        self.image=wx.StaticBitmap(panel,-1,bitmap)
        vbox2.Add(self.image,flag=wx.EXPAND,proportion=1)
        hbox.Add(vbox2,flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT,border=20,proportion=1)
        
        panel.SetSizer(hbox)

    def OnAbout(self,event):
        dlg=wx.MessageDialog(self,"点击'导航'或按下快捷键Ctrl+N选择文件打开。\n拖动滑块改变Bounding Box。",'提示')
        dlg.ShowModal()
        dlg.Destroy()

    def OnNavigation(self,event):
        dlg=wx.FileDialog(self,'选择图片','','','*.*',style=wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            directory = dlg.GetDirectory()
            file = dlg.GetFilename()
            self.path = os.path.join(directory,file)

            self.orimap=wx.Bitmap(self.path)
            dc = wx.MemoryDC(self.orimap)
            dc.SetPen(wx.Pen(wx.RED,1))
            dc.DrawLines(((50,50),(150,50),(150,100),(50,100),(50,50)))
            dc.SelectObject(wx.NullBitmap)

            bitmap=scale_bitmap(self.orimap,800,450)
            self.image.SetBitmap(bitmap)

            self.sld1.SetMax(self.orimap.GetWidth())
            self.sld1.SetValue(50)
            self.st3.SetLabel('50')

            self.sld2.SetMax(self.orimap.GetHeight())
            self.sld2.SetValue(50)
            self.st4.SetLabel('50')

            self.sld3.SetMax(self.orimap.GetWidth())
            self.sld3.SetValue(150)
            self.st5.SetLabel('150')

            self.sld4.SetMax(self.orimap.GetHeight())
            self.sld4.SetValue(100)
            self.st6.SetLabel('100')

            self.ct1.SetLabel(str(self.orimap.GetWidth()))
            self.ct2.SetLabel(str(self.orimap.GetHeight()))

        dlg.Destroy()

    def OnExit(self,event):
        self.Close(True)

    def OnSld1Scroll(self,event):
        obj = event.GetEventObject()
        val = obj.GetValue()
        self.st3.SetLabel(str(val))
        self.orimap=wx.Bitmap(self.path)
        dc = wx.MemoryDC(self.orimap)
        dc.SetPen(wx.Pen(wx.RED,1))
        x1, y1, x2, y2 = val, self.sld2.GetValue(), self.sld3.GetValue(), self.sld4.GetValue()        
        dc.DrawLines(((x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)))
        dc.SelectObject(wx.NullBitmap)
        bitmap=scale_bitmap(self.orimap,800,450)
        self.image.SetBitmap(bitmap)

    def OnSld2Scroll(self,event):
        obj = event.GetEventObject()
        val = obj.GetValue()
        self.st4.SetLabel(str(val))
        self.orimap=wx.Bitmap(self.path)
        dc = wx.MemoryDC(self.orimap)
        dc.SetPen(wx.Pen(wx.RED,1))
        x1, y1, x2, y2 = self.sld1.GetValue(), val, self.sld3.GetValue(), self.sld4.GetValue()        
        dc.DrawLines(((x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)))
        dc.SelectObject(wx.NullBitmap)
        bitmap=scale_bitmap(self.orimap,800,450)
        self.image.SetBitmap(bitmap)

    def OnSld3Scroll(self,event):
        obj = event.GetEventObject()
        val = obj.GetValue()
        self.st5.SetLabel(str(val))
        self.orimap=wx.Bitmap(self.path)
        dc = wx.MemoryDC(self.orimap)
        dc.SetPen(wx.Pen(wx.RED,1))
        x1, y1, x2, y2 = self.sld1.GetValue(), self.sld2.GetValue(), val, self.sld4.GetValue()        
        dc.DrawLines(((x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)))
        dc.SelectObject(wx.NullBitmap)
        bitmap=scale_bitmap(self.orimap,800,450)
        self.image.SetBitmap(bitmap)

    def OnSld4Scroll(self,event):
        obj = event.GetEventObject()
        val = obj.GetValue()
        self.st6.SetLabel(str(val))
        self.orimap=wx.Bitmap(self.path)
        dc = wx.MemoryDC(self.orimap)
        dc.SetPen(wx.Pen(wx.RED,1))
        x1, y1, x2, y2 = self.sld1.GetValue(), self.sld2.GetValue(), self.sld3.GetValue(), val         
        dc.DrawLines(((x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)))
        dc.SelectObject(wx.NullBitmap)
        bitmap=scale_bitmap(self.orimap,800,450)
        self.image.SetBitmap(bitmap)



app=wx.App()

frame=MainFrame(None,'显示Bounding Box的边界坐标。')
frame.Show()


app.MainLoop()