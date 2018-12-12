import wx
import keyring

class LoginPanel(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Login")

        self.SetBackgroundColour((255, 253, 208))
        self.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self.logged_in = False

        self.user_sizer = wx.GridSizer(1, 2, 0, 0)

        self.user_label = wx.StaticText(self, label="Username:")
        self.user_sizer.Add(self.user_label, 1, wx.ALL | wx.CENTER)
        self.user = wx.TextCtrl(self)
        self.user_sizer.Add(self.user, 1, wx.ALL | wx.CENTER)

        # pass info
        self.pass_sizer = wx.GridSizer(1, 2, 0, 0)

        self.pass_label = wx.StaticText(self, label="Password:")
        self.pass_sizer.Add(self.pass_label, 1, wx.ALL | wx.CENTER)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.password.Bind(wx.EVT_TEXT_ENTER, self.OnLogin)
        self.pass_sizer.Add(self.password, 1, wx.ALL | wx.CENTER)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.user_sizer, 0, wx.ALL, 5)
        self.main_sizer.Add(self.pass_sizer, 0, wx.ALL, 5)

        self.login_btn = wx.Button(self, label="Login")
        self.login_btn.Bind(wx.EVT_BUTTON, self.OnLogin)
        self.main_sizer.Add(self.login_btn, 0, wx.ALL|wx.CENTER, 5)

        self.register_btn = wx.Button(self, label="Register now!")
        self.register_btn.Bind(wx.EVT_BUTTON, self.OnRegister)
        self.main_sizer.Add(self.register_btn, 0, wx.ALL|wx.CENTER, 5)

        self.result = wx.StaticText(self, label="")
        self.main_sizer.Add(self.result, 0, wx.ALIGN_CENTER, 5)

        self.SetSizer(self.main_sizer)
        self.Show(True)

    def OnLogin(self, event):
        if keyring.get_password("emojiapp", self.user.GetValue()) == self.password.GetValue():
            self.result.SetForegroundColour((0, 255, 0))
            self.result.SetLabel("Successful Login!")
            self.logged_in = True
        else:
            self.result.SetForegroundColour((255, 0, 0))
            self.result.SetLabel("Invalid Login!")
        self.Layout()

    def OnRegister(self, event):
        self.Close()
        frame = RegisterPanel()

class RegisterPanel(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Register")

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

        self.confirm_btn = wx.Button(self, label="Confirm Register")
        self.confirm_btn.Bind(wx.EVT_BUTTON, self.OnConfirm)
        self.main_sizer.Add(self.confirm_btn, 0, wx.ALL | wx.CENTER, 5)

        self.result = wx.StaticText(self, label="")
        self.main_sizer.Add(self.result, 0, wx.ALIGN_CENTER, 5)

        self.SetSizer(self.main_sizer)
        self.Show()
    def OnConfirm(self, event):
        if len(self.user.GetValue()) == 0 or len(self.password.GetValue()) == 0:
            self.result.SetForegroundColour((255, 0, 0))
            self.result.SetLabel("Username and Password must NOT be empty!")
        elif keyring.get_password("emojiapp", self.user.GetValue()) is not None:
            self.result.SetForegroundColour((255, 0, 0))
            self.result.SetLabel("Username already in use!")
        else:
            self.result.SetForegroundColour((0, 255, 0))
            keyring.set_password("emojiapp", self.user.GetValue(), self.password.GetValue())
            self.result.SetLabel("Account created successfully!")
        self.Layout()

if __name__ == "__main__":
    app = wx.App(False)
    frame = LoginPanel(None)
    app.MainLoop()