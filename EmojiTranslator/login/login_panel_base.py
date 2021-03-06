import wx
from emoji_translator.main_app import MainWindow

class LoginPanelBase(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title)

        current_size = self.GetSize()
        self.SetSize((current_size.GetWidth() * 1.2, current_size.GetHeight()))
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
        self.login_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.main_sizer.Add(self.login_btn, 0, wx.ALL | wx.CENTER, 5)

        self.register_btn = wx.Button(self, label="Register now!")
        self.main_sizer.Add(self.register_btn, 0, wx.ALL | wx.CENTER, 5)
        self.register_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        self.guest_btn = wx.Button(self, label="Continue as guest", style=wx.BORDER_NONE)
        self.guest_btn.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, True, u'Consolas'))
        self.guest_btn.SetBackgroundColour(self.GetBackgroundColour())
        self.main_sizer.Add(self.guest_btn, 0, wx.ALL | wx.CENTER, 5)
        self.guest_btn.Bind(wx.EVT_BUTTON, self.OnGuest)
        self.guest_btn.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        self.result = wx.StaticText(self, label="")
        self.main_sizer.Add(self.result, 0, wx.ALIGN_CENTER, 5)

        self.SetSizer(self.main_sizer)
        self.Show()

    def is_pass_valid(self, password):
        has_letter = False
        has_digit = False
        for char in password:
            if not has_digit:
                has_digit = char.isdigit()
            if not has_letter:
                has_letter = char.isalpha()

        return (len(password) >= 6 and has_digit and has_letter)


    def OnRegister(self, event):
        pass

    def OnLogin(self, event):
        pass

    def OnGuest(self, event):
        confirmation_dlg = wx.MessageDialog(None,
                                            "Are you sure you want to login as guest?\nYour session settings will be lost.",
                                            "Guest login",
                                            wx.YES_NO)
        result = confirmation_dlg.ShowModal()

        if result == wx.ID_YES:
            self.Close()
            MainWindow().Show()


