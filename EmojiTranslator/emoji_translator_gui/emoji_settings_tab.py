import wx
from login.default_settings import *
from emoji_translator_gui.enums import SettingsEnum

class EmojiSettingsTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.user_settings = self.parent.user_settings

        self.SetBackgroundColour((255, 253, 208))
        self.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self.sizer = wx.FlexGridSizer(12, 1, 10, 10)
        self.settings_value_gui_dict = dict()

        title_font = self.GetFont()
        title_font.SetUnderlined(True)

        # ==================== GENERAL SETTINGS ================================
        # set title
        st = wx.StaticText(self, label="General Settings")
        st.SetFont(title_font)
        self.sizer.Add(st)

        # set attributes
        self.gen_set_sizer = wx.GridSizer(len(GENERAL_SETTINGS), 2, 10, 10)
        for setting in GENERAL_SETTINGS:
            self.gen_set_sizer.Add(wx.StaticText(self, label=setting.value), 1,
                                  wx.ALIGN_LEFT)
            value_gui = wx.ComboBox(self, choices=list(["slow", "normal", "fast"]))
            self.settings_value_gui_dict[setting] = value_gui
            self.gen_set_sizer.Add(value_gui, 0, wx.ALL, 5)

        self.sizer.Add(self.gen_set_sizer, 1, wx.ALIGN_CENTER)

        # ==================== SEARCH SETTINGS =================================
        # set title
        st = wx.StaticText(self, label="Search Tab Settings")
        st.SetFont(title_font)
        self.sizer.Add(st)

        # set attributes
        self.search_sizer = wx.GridSizer(len(SEARCH_SETTINGS), 2, 10, 10)
        for setting in SEARCH_SETTINGS:
            self.search_sizer.Add(wx.StaticText(self, label=setting.value), 1, wx.ALIGN_LEFT)
            value_gui = wx.ComboBox(self, choices=list(map(str, range(6, 41))))
            self.settings_value_gui_dict[setting] = value_gui
            self.search_sizer.Add(value_gui, 0, wx.ALL, 5)

        self.sizer.Add(self.search_sizer, 1, wx.ALIGN_CENTER)

        # ==================== DATABASE SETTINGS ===============================
        # set title
        st = wx.StaticText(self, label="Database Tab Settings")
        st.SetFont(title_font)
        self.sizer.Add(st)

        # set attributes
        self.db_sizer = wx.GridSizer(len(DB_SETTINGS), 2, 10, 10)
        for setting in DB_SETTINGS:
            self.db_sizer.Add(wx.StaticText(self, label=setting.value), 1,
                                wx.ALIGN_LEFT)
            value_gui = wx.ComboBox(self, choices=["32", "64", "128"])
            self.settings_value_gui_dict[setting] = value_gui
            self.db_sizer.Add(value_gui, 0, wx.ALL, 5)

        self.sizer.Add(self.db_sizer, 1, wx.ALIGN_CENTER)

        # ==================== TRANSLATE SETTINGS ==============================
        # set title
        st = wx.StaticText(self, label="Translation Tab Settings")
        st.SetFont(title_font)
        self.sizer.Add(st)

        # set attributes
        self.translate_sizer = wx.GridSizer(len(TRANSLATE_SETTINGS), 2, 10, 10)
        for setting in TRANSLATE_SETTINGS:
            self.translate_sizer.Add(wx.StaticText(self, label=setting.value), 1,
                              wx.ALIGN_LEFT)
            value_gui = wx.ComboBox(self, choices=list(map(str, range(6, 41))))
            self.settings_value_gui_dict[setting] = value_gui
            self.translate_sizer.Add(value_gui, 0, wx.ALL, 5)

        self.sizer.Add(self.translate_sizer, 1, wx.ALIGN_CENTER)

        # ==================== COMPOSER SETTINGS ===============================
        # set title
        st = wx.StaticText(self, label="Composer Tab Settings")
        st.SetFont(title_font)
        self.sizer.Add(st)

        # set attributes
        self.compose_sizer = wx.GridSizer(len(COMPOSE_SETTINGS), 2, 10, 10)
        for setting in COMPOSE_SETTINGS:
            self.compose_sizer.Add(wx.StaticText(self, label=setting.value), 1,
                              wx.ALIGN_LEFT)
            if setting == SettingsEnum.COMPOSER_EMOJI_SIZE:
                value_gui = wx.ComboBox(self, choices=["32", "64", "128"])
            elif setting == SettingsEnum.COMPOSER_TAB_FONT_SIZE:
                value_gui = wx.ComboBox(self, choices=list(map(str, range(6, 41))))
            self.settings_value_gui_dict[setting] = value_gui
            self.compose_sizer.Add(value_gui, 0, wx.ALL, 5)

        self.sizer.Add(self.compose_sizer, 1, wx.ALIGN_CENTER)

        # ===================== FINAL BUTTONS ==================================
        self.apply_button = wx.Button(self, label="Apply")
        self.apply_button.Bind(wx.EVT_BUTTON, self.OnApply)
        self.sizer.Add(self.apply_button, 1, wx.ALIGN_CENTER|wx.ALL)

        self.apply_result = wx.StaticText(self, label="")
        self.sizer.Add(self.apply_result, 1, wx.ALIGN_CENTER|wx.ALL)

        self.SetSizer(self.sizer)

    def OnApply(self, event):
        applied_settings = 0
        for setting in self.settings_value_gui_dict:
            current_selection = self.settings_value_gui_dict[setting].GetStringSelection()
            if current_selection != "":
                if setting != SettingsEnum.TTS_SPEED:
                    self.user_settings.settings_dict[setting] = int(current_selection)
                else:
                    self.user_settings.settings_dict[setting] = current_selection
                applied_settings += 1
        self.apply_result.SetLabel(str(applied_settings) + " setting(s) applied!")


