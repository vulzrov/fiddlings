import wx
import os

import PIL
from PIL import Image
from PIL import ImageDraw

#PIL转bitmap
def PIL_to_Bitmap(image):
    width, height = image.size
    return wx.BitmapFromBuffer(width,height,image.tobytes())

#bitmap转PIL
def Bitmap_to_PIL(bitmap):
    size = tuple(bitmap.GetSize())
    try:
        buf = size[0]*size[1]*3*'\x00'
        bitmap.CopyToBuffer(buf)
    except:
        del buf
        buf = bitmap.ConvertToImage().GetData()
    return Image.frombuffer('RGB',size,buf,'raw','RGB',0,1)

class MainFrame(wx.Frame):
    def __init__(self,parent,title='标题',size = (960,530)):
        wx.Frame.__init__(self,parent,title = title, size = size)
        #记录切片数量
        self.i = 0
        #状态栏
        self.CreateStatusBar()
        #菜单栏
        StartMenu = wx.Menu()

        About = wx.MenuItem(StartMenu,-1,'应用说明\tCtrl+A','点击或使用快捷键Ctrl+A获取应用使用说明。')
        StartMenu.Append(About)
        self.Bind(wx.EVT_MENU,self.OnAbout,About)

        Navigation = wx.MenuItem(StartMenu,-1,'导入文件\tCtrl+N','点击或使用快捷键Ctrl+N导入图像文件。')
        StartMenu.Append(Navigation)
        self.Bind(wx.EVT_MENU,self.OnNavigation,Navigation)

        Save = wx.MenuItem(StartMenu,-1,'剪切并保存图像\tCtrl+S','点击或使用快捷键Ctrl+S导出图像文件。')
        StartMenu.Append(Save)
        self.Bind(wx.EVT_MENU,self.OnOutput,Save)

        Exit = wx.MenuItem(StartMenu,-1,'退出应用\tCtrl+E','点击或使用快捷键Ctrl+E退出应用。')
        StartMenu.Append(Exit)
        self.Bind(wx.EVT_MENU,self.OnExit,Exit)

        menubar = wx.MenuBar()
        menubar.Append(StartMenu,'开始')
        self.SetMenuBar(menubar)

        #布局
        panel = wx.Panel(self)
        Hbox_Main = wx.BoxSizer()

        #操作栏
        Vbox1 = wx.BoxSizer(wx.VERTICAL)

        hbox_show_width = wx.BoxSizer()
        self.width_text = wx.StaticText(panel,-1,'宽： ')
        hbox_show_width.Add(self.width_text)
        Vbox1.Add(hbox_show_width,proportion = 1,flag = wx.BOTTOM,border = 10)

        hbox_show_height = wx.BoxSizer()
        self.height_text = wx.StaticText(panel,-1,'高： ')
        hbox_show_height.Add(self.height_text)
        Vbox1.Add(hbox_show_height,proportion = 1,flag = wx.BOTTOM, border = 10)

        hbox_slider_x1 = wx.BoxSizer()
        self.slider_x1 = wx.Slider(panel)
        self.Bind(wx.EVT_SLIDER,self.Move_Slider_x1,self.slider_x1)
        hbox_slider_x1.Add(self.slider_x1, flag = wx.RIGHT, border = 10)
        self.text_x1 = wx.StaticText(panel,-1,'0')
        hbox_slider_x1.Add(self.text_x1)
        Vbox1.Add(hbox_slider_x1,proportion = 1,flag = wx.BOTTOM,border = 10)

        hbox_slider_y1 = wx.BoxSizer()
        self.slider_y1 = wx.Slider(panel)
        self.Bind(wx.EVT_SLIDER,self.Move_Slider_y1,self.slider_y1)
        hbox_slider_y1.Add(self.slider_y1, flag = wx.RIGHT, border = 10)
        self.text_y1 = wx.StaticText(panel,-1,'0')
        hbox_slider_y1.Add(self.text_y1)
        Vbox1.Add(hbox_slider_y1,proportion = 1,flag = wx.BOTTOM,border = 10)

        hbox_slider_x2 = wx.BoxSizer()
        self.slider_x2 = wx.Slider(panel)
        self.Bind(wx.EVT_SLIDER,self.Move_Slider_x2,self.slider_x2)
        hbox_slider_x2.Add(self.slider_x2, flag = wx.RIGHT, border = 10)
        self.text_x2 = wx.StaticText(panel,-1,'0')
        hbox_slider_x2.Add(self.text_x2)
        Vbox1.Add(hbox_slider_x2,proportion = 1,flag = wx.BOTTOM,border = 10)

        hbox_slider_y2 = wx.BoxSizer()
        self.slider_y2 = wx.Slider(panel)
        self.Bind(wx.EVT_SLIDER,self.Move_Slider_y2,self.slider_y2)
        hbox_slider_y2.Add(self.slider_y2, flag = wx.RIGHT, border = 10)
        self.text_y2 = wx.StaticText(panel,-1,'0')
        hbox_slider_y2.Add(self.text_y2)
        Vbox1.Add(hbox_slider_y2,proportion = 1,flag = wx.BOTTOM,border = 10)

        hbox_buttons = wx.BoxSizer()
        Import_Button = wx.Button(panel,-1,'导入图片')
        hbox_buttons.Add(Import_Button,flag = wx.RIGHT|wx.ALIGN_CENTER,border = 10)
        self.Bind(wx.EVT_BUTTON,self.OnNavigation,Import_Button)
        Output_Button = wx.Button(panel,-1,'导出框选')
        hbox_buttons.Add(Output_Button,flag = wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON,self.OnOutput,Output_Button)
        Vbox1.Add(hbox_buttons,proportion = 1)


        Hbox_Main.Add(Vbox1, proportion = 1, flag = wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM, border = 20)

        #分割
        Hbox_Main.Add((20,-1))

        #图像显示
        Vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.image = wx.StaticBitmap(panel,size = (800,450))
        Vbox2.Add(self.image, proportion = 1, flag = wx.EXPAND)
        Hbox_Main.Add(Vbox2, proportion = 1, flag = wx.EXPAND|wx.TOP|wx.BOTTOM, border = 20)

        Hbox_Main.Add((20,-1))

        panel.SetSizer(Hbox_Main)

    def OnAbout(self,event):
        dlg = wx.MessageDialog(self,'导入文件后滑动滑块调节框选范围。之后可点击菜单栏中的“剪切并保存图像”或使用快捷键Ctrl+S保存框选部分。','说明',style = wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnNavigation(self,event):
        dlg = wx.FileDialog(self,'导入图片','','','*.*',style = wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            dir = dlg.GetDirectory()
            file = dlg.GetFilename()
            self.PIL_image = Image.open(os.path.join(dir,file),'r').convert('RGB')
            #宽高
            self.width_text.SetLabel('宽：{}'.format(self.PIL_image.width))
            self.height_text.SetLabel('高：{}'.format(self.PIL_image.height))
            #滑块初值
            self.x1 = self.PIL_image.width/4
            self.y1 = self.PIL_image.height/4
            self.x2 = self.PIL_image.width*(3/4)
            self.y2 = self.PIL_image.height*(3/4)

            self.slider_x1.SetMax(self.PIL_image.width)
            self.slider_y1.SetMax(self.PIL_image.height)
            self.slider_x2.SetMax(self.PIL_image.width)
            self.slider_y2.SetMax(self.PIL_image.height)

            self.slider_x1.SetValue(self.x1)
            self.slider_y1.SetValue(self.y1)
            self.slider_x2.SetValue(self.x2)
            self.slider_y2.SetValue(self.y2)

            #显示滑块初值
            self.text_x1.SetLabel('{}'.format(self.x1))
            self.text_y1.SetLabel('{}'.format(self.y1))
            self.text_x2.SetLabel('{}'.format(self.x2))
            self.text_y2.SetLabel('{}'.format(self.y2))
            #操作图像
            temp = self.PIL_image.copy()
            drawing = ImageDraw.Draw(temp)
            drawing.polygon([(self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2),(self.x1,self.y1)],outline='white')
            self.image.SetBitmap(PIL_to_Bitmap(temp.resize((800,450))))


        dlg.Destroy()

    def Move_Slider_x1(self,event):
        self.x1 = self.slider_x1.GetValue()
        self.text_x1.SetLabel('{}'.format(self.x1))
        temp = self.PIL_image.copy()
        drawing = ImageDraw.Draw(temp)
        drawing.polygon([(self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2),(self.x1,self.y1)],outline='white')
        self.image.SetBitmap(PIL_to_Bitmap(temp.resize((800,450))))

    def Move_Slider_y1(self,event):
        self.y1 = self.slider_y1.GetValue()
        self.text_y1.SetLabel('{}'.format(self.y1))
        temp = self.PIL_image.copy()
        drawing = ImageDraw.Draw(temp)
        drawing.polygon([(self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2),(self.x1,self.y1)],outline='white')
        self.image.SetBitmap(PIL_to_Bitmap(temp.resize((800,450))))

    def Move_Slider_x2(self,event):
        self.x2 = self.slider_x2.GetValue()
        self.text_x2.SetLabel('{}'.format(self.x2))
        temp = self.PIL_image.copy()
        drawing = ImageDraw.Draw(temp)
        drawing.polygon([(self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2),(self.x1,self.y1)],outline='white')
        self.image.SetBitmap(PIL_to_Bitmap(temp.resize((800,450))))

    def Move_Slider_y2(self,event):
        self.y2 = self.slider_y2.GetValue()
        self.text_y2.SetLabel('{}'.format(self.y2))
        temp = self.PIL_image.copy()
        drawing = ImageDraw.Draw(temp)
        drawing.polygon([(self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2),(self.x1,self.y1)],outline='white')
        self.image.SetBitmap(PIL_to_Bitmap(temp.resize((800,450))))

    def OnOutput(self,event):
        temp = self.PIL_image.crop((self.x1,self.y1,self.x2,self.y2))
        dlg = wx.DirDialog(self,'选择切片存储位置','')
        if dlg.ShowModal() == wx.ID_OK:
            dir = dlg.GetPath()
            filename = 'crop{}.jpg'.format(self.i+1)
            temp.save(os.path.join(dir,filename))
            self.i+=1

        dlg.Destroy()

    def OnExit(self,event):

        self.Close(True)





app = wx.App()

frame = MainFrame(None,'Show the bounding box')
frame.Show()

app.MainLoop()