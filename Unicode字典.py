import wx

class Str_Frame(wx.Frame):
    def __init__(self, parent, title = '翻译字符串', size = (400,400)):
        wx.Frame.__init__(self, parent, title = title, size = size)
        self.CreateStatusBar()
        #布局
        panel = wx.Panel(self)
        vbox_main = wx.BoxSizer(wx.VERTICAL)
          #输入
        hbox1 = wx.BoxSizer()
        input_sign = wx.StaticText(panel,-1,'Input: ')
        hbox1.Add(input_sign,flag = wx.RIGHT, border = 20)
        self.input_content = wx.TextCtrl(panel,-1)
        hbox1.Add(self.input_content)
        vbox_main.Add(hbox1,proportion = 0, flag = wx.TOP|wx.LEFT|wx.RIGHT,border = 20)

        vbox_main.Add((-1,20),proportion = 1)
          #翻译按钮
        hbox2 = wx.BoxSizer()
        translate = wx.Button(panel,-1,'Translate')
        hbox2.Add(translate,flag = wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON,self.OnTranslate,translate)
        vbox_main.Add(hbox2, proportion = 0, flag = wx.LEFT|wx.RIGHT,border = 20)
        vbox_main.Add((-1,20),proportion = 1)
          #二进制Unicode输出
        hbox3 = wx.BoxSizer()
        binary_sign = wx.StaticText(panel,-1,'Unicode (Binary) : ')
        hbox3.Add(binary_sign, flag = wx.RIGHT, border = 20)
        self.Binary_content = wx.TextCtrl(panel,-1)
        hbox3.Add(self.Binary_content)
        vbox_main.Add(hbox3,proportion = 0, flag = wx.LEFT|wx.RIGHT,border = 20)
        vbox_main.Add((-1,20),proportion = 1)
          #十六进制Unicode输出
        hbox4 = wx.BoxSizer()
        hexadecimal_sign = wx.StaticText(panel,-1,'Unicode (Hexadecimal) : ')
        hbox4.Add(hexadecimal_sign, flag = wx.RIGHT, border = 20)
        self.Hexadecimal_content = wx.TextCtrl(panel,-1)
        hbox4.Add(self.Hexadecimal_content)
        vbox_main.Add(hbox4, proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 20)
        vbox_main.Add((-1,20), proportion = 1)
          #十进制Unicode输出
        hbox5 = wx.BoxSizer()
        decimal_sign = wx.StaticText(panel,-1,'Unicode (Decimal) : ')
        hbox5.Add(decimal_sign,flag = wx.RIGHT, border = 20)
        self.Decimal_content = wx.TextCtrl(panel,-1)
        hbox5.Add(self.Decimal_content)
        vbox_main.Add(hbox5, proportion = 1, flag = wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 20)

        panel.SetSizer(vbox_main)

    def OnTranslate(self,event):
        s = self.input_content.GetValue()
        if len(s) > 1:
            dlg = wx.MessageDialog(self,'只能输入单个字符。','Warning')
            dlg.ShowModal()
            dlg.Destroy()
            return
        elif len(s) < 1:
            dlg = wx.MessageDialog(self,'输入为空','Warning')
            dlg.ShowModal()
            dlg.Destroy()
            return
        else:
            d = ord(s)
            self.Decimal_content.SetValue(str(d))
            b = bin(d)
            self.Binary_content.SetValue(b)
            h = hex(d)
            self.Hexadecimal_content.SetValue(h)

class Unicode_Frame(wx.Frame):
    def __init__(self, parent, title = '翻译整型Unicode', size = (400,300)):
        wx.Frame.__init__(self, parent, title = title, size = size)
        self.CreateStatusBar()
        #布局
        panel = wx.Panel(self)
        vbox_main = wx.BoxSizer(wx.VERTICAL)
          #输入
        hbox1 = wx.BoxSizer()
        input_sign = wx.StaticText(panel,-1,'Input (decimal): ')
        hbox1.Add(input_sign,flag = wx.RIGHT, border = 20)
        self.input_content = wx.TextCtrl(panel,-1)
        hbox1.Add(self.input_content)
        vbox_main.Add(hbox1,proportion = 0, flag = wx.TOP|wx.LEFT|wx.RIGHT,border = 20)

        vbox_main.Add((-1,20),proportion = 1)
          #翻译按钮
        hbox2 = wx.BoxSizer()
        translate = wx.Button(panel,-1,'Translate')
        hbox2.Add(translate,flag = wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON,self.OnTranslate,translate)
        vbox_main.Add(hbox2, proportion = 0, flag = wx.LEFT|wx.RIGHT,border = 20)
        vbox_main.Add((-1,20),proportion = 1)
          #字符串输出
        hbox3 = wx.BoxSizer()
        str_sign = wx.StaticText(panel,-1,'String : ')
        hbox3.Add(str_sign, flag = wx.RIGHT, border = 20)
        self.Str_content = wx.TextCtrl(panel,-1)
        hbox3.Add(self.Str_content)
        vbox_main.Add(hbox3,proportion = 0, flag = wx.BOTTOM|wx.LEFT|wx.RIGHT,border = 20)

        panel.SetSizer(vbox_main)

    def OnTranslate(self,event):
        d = self.input_content.GetValue()
        try:
            s = chr(int(d))
            self.Str_content.SetValue(s)
        except:
            dlg = wx.MessageDialog(self,'输入有误，请输入十进制数。','Warning')
            dlg.ShowModal()
            dlg.Destroy()

class Convert_Frame(wx.Frame):
    def __init__(self, parent, title = '进制转换', size = (400,300)):
        wx.Frame.__init__(self, parent, title = title, size = size)
        self.CreateStatusBar()
        #布局
        panel = wx.Panel(self)
        vbox_main = wx.BoxSizer(wx.VERTICAL)

          #二进制
        hbox1 = wx.BoxSizer()
        binary_sign = wx.StaticText(panel,-1,'Binary : ')
        hbox1.Add(binary_sign, flag = wx.RIGHT, border = 20)
        self.Binary_content = wx.TextCtrl(panel,-1)
        hbox1.Add(self.Binary_content)
        vbox_main.Add(hbox1,proportion = 0, flag = wx.TOP|wx.LEFT|wx.RIGHT,border = 20)
        vbox_main.Add((-1,20),proportion = 1)
          #十六进制
        hbox2 = wx.BoxSizer()
        hexadecimal_sign = wx.StaticText(panel,-1,'Hexadecimal : ')
        hbox2.Add(hexadecimal_sign, flag = wx.RIGHT, border = 20)
        self.Hexadecimal_content = wx.TextCtrl(panel,-1)
        hbox2.Add(self.Hexadecimal_content)
        vbox_main.Add(hbox2, proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 20)
        vbox_main.Add((-1,20), proportion = 1)
          #十进制
        hbox3 = wx.BoxSizer()
        decimal_sign = wx.StaticText(panel,-1,'Decimal : ')
        hbox3.Add(decimal_sign,flag = wx.RIGHT, border = 20)
        self.Decimal_content = wx.TextCtrl(panel,-1)
        hbox3.Add(self.Decimal_content)
        vbox_main.Add(hbox3, proportion = 1, flag = wx.LEFT|wx.RIGHT, border = 20)
        vbox_main.Add((-1,20),proportion = 1)
          #翻译按钮
        hbox4 = wx.BoxSizer()
        translate = wx.Button(panel,-1,'Translate')
        hbox4.Add(translate,flag = wx.RIGHT,border = 20)
        self.Bind(wx.EVT_BUTTON,self.OnTranslate,translate)
        reset = wx.Button(panel,-1,'Reset')
        hbox4.Add(reset)
        self.Bind(wx.EVT_BUTTON,self.OnClear,reset)
        vbox_main.Add(hbox4, proportion = 0, flag = wx.BOTTOM|wx.LEFT|wx.RIGHT,border = 20)
        
        panel.SetSizer(vbox_main)

    def OnTranslate(self,event):
        b = self.Binary_content.GetValue()
        h = self.Hexadecimal_content.GetValue()
        d = self.Decimal_content.GetValue()
        if len(b) != 0:
            d = int(b,2)
            h = hex(d)
            self.Decimal_content.SetValue(str(d))
            self.Hexadecimal_content.SetValue(h)
            return
        elif len(h) != 0:
            d = int(h,16)
            b = bin(d)
            self.Decimal_content.SetValue(str(d))
            self.Binary_content.SetValue(b)
            return
        elif len(d) != 0:
            b = bin(int(d))
            h = hex(int(d))
            self.Binary_content.SetValue(b)
            self.Hexadecimal_content.SetValue(h)
            return
        else:
            dlg = wx.MessageDialog(self,'输入为空','Warning')
            dlg.ShowModal()
            dlg.Destroy()
            return

    def OnClear(self,event):
        self.Binary_content.SetValue('')
        self.Hexadecimal_content.SetValue('')
        self.Decimal_content.SetValue('')


class MainFrame(wx.Frame):
    def __init__(self, parent, title = 'Unicode字典', size = (200,300)):
        wx.Frame.__init__(self, parent, title = title, size = size)
        self.CreateStatusBar()

        #菜单栏
        filemenu = wx.Menu()
          #帮助
        About = wx.MenuItem(filemenu,-1,'About\tCtrl+D','帮助')
        filemenu.Append(About)
        self.Bind(wx.EVT_MENU,self.OnAbout,About)
          #选择模式
        Models = wx.Menu()
            #字符串翻Unicode
        str_to_unicode = wx.MenuItem(Models,-1,'字符串翻Unicode\tCtrl+J')
        Models.Append(str_to_unicode)
        self.Bind(wx.EVT_MENU,self.On_mode_str_to_uni,str_to_unicode)
            #Unicode翻字符串
        unicode_to_str = wx.MenuItem(Models,-1,'Unicode翻字符串\tCtrl+K')
        Models.Append(unicode_to_str)
        self.Bind(wx.EVT_MENU,self.On_mode_uni_to_str,unicode_to_str)
            #进制转换
        convertion = wx.MenuItem(Models,-1,'进制转换\tCtrl+L')
        Models.Append(convertion)
        self.Bind(wx.EVT_MENU,self.On_mode_convertion,convertion)
        filemenu.Append(-1,'Models',Models,'选择模式')
          #退出
        Exit = wx.MenuItem(filemenu,-1,'Exit\tCtrl+E','退出')
        filemenu.Append(Exit)
        self.Bind(wx.EVT_MENU,self.OnExit,Exit)

        menubar = wx.MenuBar()
        menubar.Append(filemenu,'file')
        self.SetMenuBar(menubar)

        #布局
        panel = wx.Panel(self)
        Vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer()
        mode_str_to_uni = wx.Button(panel,-1,'字符串翻Unicode')
        hbox1.Add(mode_str_to_uni,flag = wx.ALIGN_CENTER|wx.BOTTOM,border = 20)
        self.Bind(wx.EVT_BUTTON,self.On_mode_str_to_uni,mode_str_to_uni)
        Vbox.Add(hbox1, proportion = 1, flag = wx.TOP|wx.RIGHT|wx.LEFT, border = 20)

        hbox2 = wx.BoxSizer()
        mode_uni_to_str = wx.Button(panel,-1,'Unicode翻字符串')
        hbox2.Add(mode_uni_to_str,flag = wx.ALIGN_CENTER|wx.BOTTOM,border = 20)
        self.Bind(wx.EVT_BUTTON,self.On_mode_uni_to_str,mode_uni_to_str)
        Vbox.Add(hbox2, proportion = 1, flag = wx.RIGHT|wx.LEFT, border = 20)

        hbox3 = wx.BoxSizer()
        mode_convertion = wx.Button(panel,-1,'进制转换')
        hbox3.Add(mode_convertion, flag = wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON,self.On_mode_convertion,mode_convertion)
        Vbox.Add(hbox3, proportion = 1, flag = wx.BOTTOM|wx.RIGHT|wx.LEFT, border = 20)

        panel.SetSizer(Vbox)

    #帮助
    def OnAbout(self,event):
        dlg = wx.MessageDialog(self,'应用共三个模式：字符串转Unicode/unicode转字符串/和进制换算。点击按钮选择模式。','帮助')
        dlg.ShowModal()
        dlg.Destroy()

    #模式：字符串翻Unicode
    def On_mode_str_to_uni(self,event):
        str_frame = Str_Frame(self)
        str_frame.Show()

    #模式：Unicode翻字符串
    def On_mode_uni_to_str(self,event):
        str_frame = Unicode_Frame(self)
        str_frame.Show()

    #模式：进制转换
    def On_mode_convertion(self,event):
        str_frame = Convert_Frame(self)
        str_frame.Show()

    #强制退出
    def OnExit(self,event):

        self.Close(True)
       

app = wx.App()
frame = MainFrame(None)
frame.Show()
app.MainLoop()