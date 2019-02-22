import wx
import os
import sys
import pickle
from emoji_translator_gui.emoji_db_tab import EmojiDBTab
from emoji_translator_gui.emoji_search_tab import EmojiSearchTab
from emoji_translator_gui.emoji_translation_tab import *
from emoji_translator_gui.emoji_compose_tab import EmojiComposeTab
from emoji_translator_gui.emoji_settings_tab import EmojiSettingsTab
from emoji_translator_gui.enums import *
from login.settings import Settings

class MainWindow(wx.Frame):
    def __init__(self, username="guest"):
        wx.Frame.__init__(self, None, title="Emoji Translator")

        self.username = username
        self.user_profile = self.get_user_profile()
        self.user_settings = self.user_profile["settings"]
        self.user_profile["settings"] = self.user_settings

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.sizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0, 1)
        self.sizer.AddGrowableCol(1, 80)

        self.buttons_panel = wx.Panel(self)
        self.buttons_sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttons_panel.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self.search_button = wx.ToggleButton(self.buttons_panel, label=Tab.SEARCH.value)
        self.db_button = wx.ToggleButton(self.buttons_panel, label=Tab.DATABASE.value)
        self.translate_button = wx.ToggleButton(self.buttons_panel, label=Tab.TRANSLATE.value)
        self.composer_button = wx.ToggleButton(self.buttons_panel, label=Tab.COMPOSE.value)
        self.settings_button = wx.ToggleButton(self.buttons_panel, label=Tab.SETTINGS.value)
        self.settings_button.SetFont(self.settings_button.GetFont().MakeBold())

        self.options_button_list = list([self.search_button, self.db_button,
                                         self.translate_button, self.composer_button, self.settings_button])

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
        self.buttons_sizer.Add(self.composer_button, 0, wx.ALL, 5)
        self.buttons_sizer.AddSpacer(50)
        self.buttons_sizer.Add(self.settings_button, 0, wx.ALL, 5)
        self.buttons_sizer.AddSpacer(15)

        self.buttons_panel.SetSizer(self.buttons_sizer)

        self.main_panel = EmojiSearchTab(self)
        self.search_button.SetValue(True)
        self.search_button.SetBackgroundColour((192, 192, 192))

        self.sizer.Add(self.buttons_panel, 1, wx.EXPAND)
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.current_saved_composer_text = ""
        self.translation_direction = TranslationDirection.FROM_EMOJI_TO_TEXT
        self.current_saved_translation_text = ""

        self.Show(True)
        self.SetSize((wx.GetDisplaySize().width * 0.55, wx.GetDisplaySize().height * 0.9))

    def get_panel_by_name(self, name):
        if name == Tab.SEARCH.value:
            return EmojiSearchTab(self)
        elif name == Tab.TRANSLATE.value:
            return EmojiTranslationTab(self, saved_text=self.current_saved_translation_text, translation_direction=self.translation_direction)
        elif name == Tab.DATABASE.value:
            return EmojiDBTab(self)
        elif name == Tab.COMPOSE.value:
            return EmojiComposeTab(self, saved_text=self.current_saved_composer_text)
        else:
            return EmojiSettingsTab(self)

    def OnNewPress(self, event):
        if type(self.main_panel) is EmojiComposeTab:
            self.current_saved_composer_text = self.main_panel.editor.GetValue()
        elif type(self.main_panel) is EmojiTranslationTab and self.main_panel.translation_direction == TranslationDirection.FROM_EMOJI_TO_TEXT:
            self.current_saved_translation_text = self.main_panel.out_text.GetValue()
            self.translation_direction = self.main_panel.translation_direction
        elif type(self.main_panel) is EmojiTranslationTab and self.main_panel.translation_direction == TranslationDirection.FROM_TEXT_TO_EMOJI:
            self.current_saved_translation_text = self.main_panel.user_input.GetValue()
            self.translation_direction = self.main_panel.translation_direction
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

    def OnClose(self, event):
        if self.username != "guest":
            profile_path = os.path.join(os.getcwd(), "../user_profiles",
                                        self.username + ".pickle")
            if not os.path.exists(os.path.join(os.getcwd(), "../user_profiles")):
                os.makedirs(os.path.join(os.getcwd(), "../user_profiles"))
            with open(profile_path, 'wb') as f:
                pickle.dump(self.user_profile, f, protocol=pickle.HIGHEST_PROTOCOL)
        event.Skip()

    def get_user_profile(self):
        profile_path = os.path.join(os.getcwd(), "../user_profiles", self.username + ".pickle")
        if os.path.isfile(profile_path):
            with open(profile_path, 'rb') as f:
                return pickle.load(f)
        else:
            return dict({
                "username" : self.username,
                "settings" : Settings(self.username),
                "saved_messages" : list()
            })

if __name__ == "__main__":
    app = wx.App(False)
    from login.login_panels import LoginPanel
    frame = LoginPanel()
    app.MainLoop()