import wx
import os

def s_to_l(str1):
    L_str1=[]
    for char in str1:
        L_str1.append(char)
    return L_str1

def exchange(str1,str2,str3):
    result=[]
    if str2 =='**SPACE**':
        str2 = ' '
    L_str1=s_to_l(str1)
    L_str2=s_to_l(str2)
    L_str3=s_to_l(str3)
    i=0
    while( i < len(str1)):
        if ( i < len(str1)-len(str2)+1) and (L_str1[i:i+len(str2)]==L_str2):
            result+=L_str3
            i+=len(str2)
        else:
            result.append(L_str1[i])
            i+=1

    return ''.join(result)    

class MainFrame(wx.Frame):
    def __init__(self, parent, title = '字符转换器', size = (1080, 690)):
        wx.Frame.__init__(self, parent, title = title, size = size)
        self.CreateStatusBar()

        #菜单栏
        filemenu = wx.Menu()

        About = wx.MenuItem(filemenu,-1,'About\tCtrl+A','帮助')
        filemenu.Append(About)
        self.Bind(wx.EVT_MENU,self.OnAbout,About)

        Browse = wx.MenuItem(filemenu,-1,'Browse\tCtrl+B','浏览')
        filemenu.Append(Browse)
        self.Bind(wx.EVT_MENU,self.OnBrowse,Browse)

        Save = wx.MenuItem(filemenu,-1,'Save\tCtrl+S','保存')
        filemenu.Append(Save)
        self.Bind(wx.EVT_MENU,self.OnSave,Save)

        Cover = wx.MenuItem(filemenu,-1,'Cover\tCtrl+F','Cover')
        filemenu.Append(Cover)
        self.Bind(wx.EVT_MENU,self.OnCover,Cover)

        Exit = wx.MenuItem(filemenu,-1,'Exit\tCtrl+E','退出')
        filemenu.Append(Exit)
        self.Bind(wx.EVT_MENU,self.OnExit,Exit)
        menubar = wx.MenuBar()
        menubar.Append(filemenu,'file')
        self.SetMenuBar(menubar)

        #布局
        panel = wx.Panel(self)
        Hbox_Main = wx.BoxSizer()

          #输入框
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        Input_Sign = wx.StaticText(panel,-1,'输入')
        vbox1.Add(Input_Sign, flag = wx.BOTTOM, border = 10)
        self.Input_Content = wx.TextCtrl(panel,style = wx.TE_MULTILINE, size = (400,600))
        vbox1.Add(self.Input_Content, flag = wx.EXPAND)
        Hbox_Main.Add(vbox1,proportion = 0,flag = wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.TOP, border = 20)

        Hbox_Main.Add((20,-1),proportion = 1)
          #控制台
        vbox2 = wx.BoxSizer(wx.VERTICAL)

            #From:
        hbox1 = wx.BoxSizer()
        From_Sign = wx.StaticText(panel,-1,'From: ')
        hbox1.Add(From_Sign,flag = wx.RIGHT, border = 10)
        self.From_Input = wx.TextCtrl(panel)
        hbox1.Add(self.From_Input,flag = wx.EXPAND)
        vbox2.Add(hbox1,flag = wx.BOTTOM,border = 40)
            #To:
        hbox2 = wx.BoxSizer()
        To_Sign = wx.StaticText(panel,-1,'To:     ')
        hbox2.Add(To_Sign,flag = wx.RIGHT, border = 10)
        self.To_Input = wx.TextCtrl(panel)
        hbox2.Add(self.To_Input,flag = wx.EXPAND)
        vbox2.Add(hbox2,flag = wx.BOTTOM,border = 40)
            #Browse
        self.Browse = wx.Button(panel,-1,'Browse')
        vbox2.Add(self.Browse,flag = wx.ALIGN_CENTER|wx.BOTTOM,border = 40)
        self.Bind(wx.EVT_BUTTON,self.OnBrowse,self.Browse)
            #Start
        self.Start = wx.Button(panel,-1,'Start')
        vbox2.Add(self.Start,flag = wx.ALIGN_CENTER|wx.BOTTOM,border = 40)
        self.Bind(wx.EVT_BUTTON,self.OnTransform,self.Start)
            #覆盖
        self.Cover = wx.Button(panel,-1,'Cover')
        vbox2.Add(self.Cover,flag = wx.ALIGN_CENTER|wx.BOTTOM,border = 40)
        self.Bind(wx.EVT_BUTTON,self.OnCover,self.Cover)
            #Save
        self.Save = wx.Button(panel,-1,'Save')
        vbox2.Add(self.Save,flag = wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON,self.OnSave,self.Save)


        Hbox_Main.Add(vbox2 ,proportion = 0,flag = wx.EXPAND|wx.TOP, border = 130)

        Hbox_Main.Add((20,-1),proportion = 1)

          #输出框
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        Output_Sign = wx.StaticText(panel,-1,'输出')
        vbox3.Add(Output_Sign, flag = wx.BOTTOM, border = 10)
        self.Output_Content = wx.TextCtrl(panel,-1,style = wx.TE_MULTILINE, size = (400,600))
        vbox3.Add(self.Output_Content, flag = wx.EXPAND)
        Hbox_Main.Add(vbox3,proportion = 0,flag = wx.EXPAND|wx.RIGHT|wx.BOTTOM|wx.TOP, border = 20)


        panel.SetSizer(Hbox_Main)

    #获取帮助
    def OnAbout(self,event):
        dlg = wx.MessageDialog(self,'点击browse导入文本文件或直接在左侧文本框中输入。之后点击start键获取结果。','帮助')
        dlg.ShowModal()
        dlg.Destroy()

    #浏览文件夹并导入文本文件
    def OnBrowse(self,event):
        dlg = wx.FileDialog(self,'导入文件','','','*.txt',style = wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            directory = dlg.GetDirectory()
            filename = dlg.GetFilename()
            with open(os.path.join(directory,filename),'r',encoding = 'utf-8') as f:
                self.Input_Content.SetValue(f.read())
        dlg.Destroy()

    #覆盖输入
    def OnCover(self,event):

        self.Input_Content.SetValue(self.Output_Content.GetValue())

    #进行转换
    def OnTransform(self,event):
        F = self.From_Input.GetValue()
        if len(F) < 1:
            dlg = wx.MessageDialog(self,'请指定你想替换的字符串，用空格隔开。如果要替换空格，请输入**SPACE**。','警告')
            dlg.ShowModal()
            dlg.Destroy()
            return
        Input = self.Input_Content.GetValue()
        F = F.strip().split()
        T = self.To_Input.GetValue().strip().split()
        if len(T)  == 0:
            for from_word in F:
                Input = exchange(Input,from_word,'')
            self.Output_Content.SetValue(Input)
        elif len(F) != len(T):
            dlg = wx.MessageDialog(self,'输入不对称。','警告')
            dlg.ShowModal()
            dlg.Destroy()
        else:
            zips = zip(F,T)
            for from_word,to_word in zips:
                Input = exchange(Input,from_word,to_word)
            self.Output_Content.SetValue(Input)
        


    #存储输出
    def OnSave(self,event):
        dlg = wx.DirDialog(self,'浏览','',style = wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            directory = dlg.GetPath()
            filename = 'output.txt'
            with open(os.path.join(directory,filename),'w',encoding = 'utf-8') as f:
                f.write(self.Output_Content.GetValue())
            remind_dlg = wx.MessageDialog(self,'Successfully Saved!','Reminder')
            remind_dlg.ShowModal()
            remind_dlg.Destroy()

        dlg.Destroy()

    #强制退出
    def OnExit(self,event):

        self.Close(True)


app = wx.App()

frame = MainFrame(None)
frame.Show()

app.MainLoop()