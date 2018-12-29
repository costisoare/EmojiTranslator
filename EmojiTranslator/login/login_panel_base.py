import wx

class LoginPanelBase(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)

        self.SetBackgroundColour((255, 253, 208))
        self.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self.user_sizer = wx.GridSizer(1, 2, 0, 0)
        self.user_label = wx.StaticText(self, label="Username:")
        self.user_sizer.Add(self.user_label, 1, wx.ALL | wx.CENTER, 5)
        self.user = wx.TextCtrl(self)
        self.user_sizer.Add(self.user, 1, wx.ALL, 5)

        self.pass_sizer = wx.GridSizer(1, 2, 0, 0)

        self.pass_label = wx.StaticText(self, label="Password:")
        self.pass_sizer.Add(self.pass_label, 0, wx.ALL | wx.CENTER, 5)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.pass_sizer.Add(self.password, 0, wx.ALL, 5)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.user_sizer, 0, wx.ALL, 5)
        self.main_sizer.Add(self.pass_sizer, 0, wx.ALL, 5)

        self.login_btn = wx.Button(self, label="Login")
        self.main_sizer.Add(self.login_btn, 0, wx.ALL | wx.CENTER, 5)

        self.register_btn = wx.Button(self, label="Register now!")
        self.main_sizer.Add(self.register_btn, 0, wx.ALL | wx.CENTER, 5)

        self.result = wx.StaticText(self, label="")
        self.main_sizer.Add(self.result, 0, wx.ALIGN_CENTER, 5)

        self.SetSizer(self.main_sizer)
        self.Show()

    def OnRegister(self, event):
        pass

    def OnLogin(self, event):
        pass