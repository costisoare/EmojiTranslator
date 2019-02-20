import wx
import keyring
from login.login_panel_base import LoginPanelBase

class LoginPanel(LoginPanelBase):
    def __init__(self):
        LoginPanelBase.__init__(self, title="Login")
        self.logged_in = False

        self.password.Bind(wx.EVT_TEXT_ENTER, self.OnLogin)

        self.login_btn.Bind(wx.EVT_BUTTON, self.OnLogin)
        self.register_btn.Bind(wx.EVT_BUTTON, self.OnRegister)
        self.register_btn.SetLabel("Create an account now!")
        self.Layout()

    def OnLogin(self, event):
        if keyring.get_password("emojiapp", self.user.GetValue()) == self.password.GetValue():
            self.result.SetForegroundColour((0, 255, 0))
            self.result.SetLabel("Successful Login!")
            self.logged_in = True
            from emoji_translator.main_app import MainWindow
            MainWindow(self.user.GetValue()).Show()
            self.Close()
        else:
            self.result.SetForegroundColour((255, 0, 0))
            self.result.SetLabel("Invalid Login!")
        self.Layout()

    def OnRegister(self, event):
        self.Close()
        RegisterPanel().Show()

class RegisterPanel(LoginPanelBase):
    def __init__(self):
        LoginPanelBase.__init__(self, title="Register")

        self.login_btn.SetLabel("Back to Login")
        self.password.Bind(wx.EVT_TEXT_ENTER, self.OnRegister)

        self.login_btn.Bind(wx.EVT_BUTTON, self.OnLogin)
        self.register_btn.Bind(wx.EVT_BUTTON, self.OnRegister)

        self.pass_guideline = wx.StaticText(self, label="Password must:\n"
                                                        "- Be at least 6 characters long\n"
                                                        "- Contain at least a digit (0-9)\n"
                                                        "- Contain at least a letter (a-z, A-Z)")
        self.main_sizer.Add(self.pass_guideline, 0, wx.ALL | wx.CENTER, 5)
        self.Layout()

    def OnRegister(self, event):
        if len(self.user.GetValue()) == 0 or len(self.password.GetValue()) == 0:
            self.result.SetForegroundColour((255, 0, 0))
            self.result.SetLabel("Username and Password must NOT be empty!")
        elif keyring.get_password("emojiapp", self.user.GetValue()) is not None:
            self.result.SetForegroundColour((255, 0, 0))
            self.result.SetLabel("Username already in use!")
        elif not self.is_pass_valid(self.password.GetValue()):
            self.result.SetForegroundColour((255, 0, 0))
            self.result.SetLabel("Password is not strong enough.")
        else:
            self.result.SetForegroundColour((0, 255, 0))
            keyring.set_password("emojiapp", self.user.GetValue(), self.password.GetValue())
            self.result.SetLabel("Account created successfully!")
            self.login_btn.Show()
            self.register_btn.Hide()
        self.Layout()

    def OnLogin(self, event):
        self.Close()
        LoginPanel().Show()