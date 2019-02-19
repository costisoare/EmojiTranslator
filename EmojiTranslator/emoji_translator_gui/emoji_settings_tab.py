import wx
from login.default_settings import SETTINGS
from emoji_translator_gui.enums import SettingsEnum

class EmojiSettingsTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.user_settings = self.parent.user_settings

        self.SetBackgroundColour((255, 253, 208))
        self.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self.sizer = wx.FlexGridSizer(len(SETTINGS.keys()) + 2, 2, 10, 10)
        self.sizer.AddSpacer(15)
        self.sizer.AddSpacer(15)

        self.settings_value_gui_dict = dict()
        for setting in SETTINGS.keys():
            self.sizer.Add(wx.StaticText(self, label=setting.value), 1, wx.ALIGN_LEFT)

            if setting in [SettingsEnum.DB_EMOJI_SIZE, SettingsEnum.COMPOSER_EMOJI_SIZE]:
                value_gui = wx.ComboBox(self, choices=["32", "64", "128"])
            elif setting == SettingsEnum.SEARCH_TAB_FONT_SIZE:
                font_sizes = list(map(str, range(6, 40)))
                value_gui = wx.ComboBox(self, choices=font_sizes)

            self.sizer.Add(value_gui, 0, wx.ALL, 5)
            self.settings_value_gui_dict[setting] = value_gui

        self.apply_button = wx.Button(self, label="Apply")
        self.apply_button.Bind(wx.EVT_BUTTON, self.OnApply)
        self.sizer.Add(self.apply_button, 1, wx.ALIGN_CENTER)

        self.apply_result = wx.StaticText(self, label="")
        self.sizer.Add(self.apply_result, 1, wx.ALIGN_CENTER)

        self.SetSizer(self.sizer)

    def OnApply(self, event):
        applied_settings = 0
        for setting in self.settings_value_gui_dict:
            current_selection = self.settings_value_gui_dict[setting].GetStringSelection()
            if current_selection != "":
                self.user_settings.settings_dict[setting] = int(current_selection)
                applied_settings += 1
        self.apply_result.SetLabel(str(applied_settings) + " setting(s) applied!")


