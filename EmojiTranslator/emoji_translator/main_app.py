import wx

from emoji_translator_gui.emoji_db_tab import EmojiDBTab
from emoji_translator_gui.emoji_search_tab import EmojiSearchTab
from emoji_translator_gui.emoji_translation_tab import EmojiTranslationTab

class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Emoji Translator")

        self.sizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0, 1)
        self.sizer.AddGrowableCol(1, 80)

        self.buttons_panel = wx.Panel(self)
        self.buttons_sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttons_panel.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self.search_button = wx.ToggleButton(self.buttons_panel, label='Search')
        self.db_button = wx.ToggleButton(self.buttons_panel, label='Database')
        self.translate_button = wx.ToggleButton(self.buttons_panel, label='Translate')
        self.options_button_list = list([self.search_button, self.db_button, self.translate_button])

        for button in self.options_button_list:
            button.SetBackgroundColour(self.buttons_panel.GetBackgroundColour())
            button.Bind(wx.EVT_TOGGLEBUTTON, self.OnNewPress)

        self.buttons_sizer.AddSpacer(15)
        self.buttons_sizer.Add(self.search_button, 0, wx.ALL, 5)
        self.buttons_sizer.AddSpacer(15)
        self.buttons_sizer.Add(self.db_button, 0, wx.ALL, 5)
        self.buttons_sizer.AddSpacer(15)
        self.buttons_sizer.Add(self.translate_button, 0, wx.ALL, 5)
        self.buttons_sizer.AddSpacer(15)
        self.buttons_panel.SetSizer(self.buttons_sizer)

        self.main_panel = EmojiSearchTab(self)
        self.search_button.SetValue(True)
        self.search_button.SetBackgroundColour((192, 192, 192))

        self.sizer.Add(self.buttons_panel, 1, wx.EXPAND)
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Show(True)
        self.SetSize((wx.GetDisplaySize().width * 0.45, wx.GetDisplaySize().height * 0.9))

    def get_panel_by_name(self, name):
        if name == 'Translate':
            return EmojiTranslationTab(self)
        elif name == 'Database':
            return EmojiDBTab(self)
        else:
            return EmojiSearchTab(self)

    def OnNewPress(self, event):
        self.main_panel.Destroy()
        pressed_button = event.GetEventObject()
        pressed_button.SetBackgroundColour((192, 192, 192))

        new_tab_name = pressed_button.GetLabel()
        self.main_panel = self.get_panel_by_name(new_tab_name)

        for button in self.options_button_list:
            if button is not pressed_button:
                button.SetValue(False)
                button.SetBackgroundColour(self.buttons_panel.GetBackgroundColour())
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        self.Layout()

