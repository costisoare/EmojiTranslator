import wx
from wx.lib.scrolledpanel import ScrolledPanel

from emoji_translator_utils.emoji_categ_parser import *
from emoji_translator_utils.emoji_dict_utils import *
from emoji_translator_gui.emoji_gui_utils import EmojiBitmap

class EmojiDBTab(wx.Panel):
    def __init__(self, parent, composer=False):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self.user_settings = self.parent.user_settings
        self.user_profile = self.parent.user_profile

        self.SetBackgroundColour(self.user_settings.get_background_color())
        self.emoji_categories = emoji_categs_from_file()
        if self.user_profile.username != "guest":
            self.emoji_categories["most_used"] = list(self.user_profile.used_emojis.keys())
        self.emoji_categ_buttons = dict()

        self.dbtab_sizer = wx.FlexGridSizer(3, 1, 0, 0)
        self.dbtab_sizer.AddGrowableRow(2)
        self.dbtab_sizer.AddGrowableCol(0)

        self.button_sizer = wx.GridSizer(1, len(self.emoji_categories), 0, 0)
        self.emoji_bmps_panel = wx.Panel()

        self.composer = composer

        self.dbtab_sizer.Add(self.button_sizer, 1, wx.EXPAND)
        self.dbtab_sizer.AddSpacer(10)
        if self.user_profile.username != "guest":
            mostused_bmp_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                         'gui_utils_files', 'most_used.png')
            most_used_bmp = wx.Bitmap(mostused_bmp_file).ConvertToImage()
            most_used_bmp = most_used_bmp.Scale(self.user_settings.get_composer_emoji_size() if self.composer else self.user_settings.get_db_emoji_size(),
                                                self.user_settings.get_composer_emoji_size() if self.composer else self.user_settings.get_db_emoji_size(),
                                                wx.IMAGE_QUALITY_HIGH)
            self.emoji_categ_buttons["most_used"] = wx.BitmapToggleButton(self,
                                                                  label=wx.Bitmap(most_used_bmp),
                                                                  name="most_used",
                                                                  style=wx.BORDER_NONE)
            self.emoji_categ_buttons["most_used"].Bind(wx.EVT_TOGGLEBUTTON, self.OnEmojiCategory)
            self.emoji_categ_buttons["most_used"].SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.emoji_categ_buttons["most_used"].SetBackgroundColour((255, 255, 255))
            self.button_sizer.Add(self.emoji_categ_buttons["most_used"], 1, wx.EXPAND)

        for cat in self.emoji_categories:
            if cat != "most_used":
                bmp_path = unicode_to_filename(STRING_UNICODE[self.emoji_categories[cat][0]],
                                               self.user_settings.get_composer_emoji_size() if self.composer else self.user_settings.get_db_emoji_size())
                self.emoji_categ_buttons[cat] = wx.BitmapToggleButton(self, label=wx.Bitmap(bmp_path),
                                                                      name=cat, style=wx.BORDER_NONE)
                self.emoji_categ_buttons[cat].Bind(wx.EVT_TOGGLEBUTTON, self.OnEmojiCategory)
                self.emoji_categ_buttons[cat].SetCursor(wx.Cursor(wx.CURSOR_HAND))
                self.emoji_categ_buttons[cat].SetBackgroundColour((255, 255, 255))
                self.button_sizer.Add(self.emoji_categ_buttons[cat], 1, wx.EXPAND)

        self.SetSizer(self.dbtab_sizer)

    def OnEmojiCategory(self, event):
        pressed_button = event.GetEventObject()
        pressed_button.SetBackgroundColour((105, 105, 105))
        for cat in self.emoji_categ_buttons:
            if not (self.emoji_categ_buttons[cat] is pressed_button):
                self.emoji_categ_buttons[cat].SetValue(False)
                self.emoji_categ_buttons[cat].SetBackgroundColour((255, 255, 255))

        self.populate_grid_with_emojis(pressed_button.GetName())
        self.Layout()

    def OnComposerClickEmoji(self, event):
        self.parent.clicked_composer_emoji = self.clicked_composer_emoji
        self.parent.OnComposerClickEmoji(event)

    def populate_grid_with_emojis(self, category):
        self.emoji_bmps_panel.Destroy()
        if self.user_profile.username != "guest":
            sorted_most_used = [x[0] for x in sorted(self.user_profile.used_emojis.items(), key=lambda kv: kv[1], reverse=True)]
            self.emoji_categories["most_used"] = sorted_most_used
        self.emoji_bmps_panel = EmojiPanel(self, category, self.emoji_categories[category], composer=self.composer)
        self.dbtab_sizer.Add(self.emoji_bmps_panel, 1, wx.EXPAND|wx.ALIGN_LEFT)

class EmojiPanel(ScrolledPanel):
    def __init__(self, parent, category, category_list, composer=False):
        ScrolledPanel.__init__(self, parent)
        self.parent = parent
        self.composer = composer
        self.SetupScrolling()
        self.Show(False)
        self.emoji_size = self.parent.user_settings.get_composer_emoji_size() if self.parent.composer else self.parent.user_settings.get_db_emoji_size()
        if category != "most_used":
            self.sizer = wx.GridSizer(len(category_list) / len(self.parent.emoji_categ_buttons.keys()) + 1, len(self.parent.emoji_categ_buttons.keys()), 15, 0)
            self.add_emojis_to_panel(category_list)
        else:
            self.sizer = wx.GridSizer(len(category_list) / len(self.parent.emoji_categ_buttons.keys()) + 1, len(self.parent.emoji_categ_buttons.keys()), 15, 0)
            self.add_most_used_emojis(category_list)
        self.sizer.SetRows(self.realnum_emojis / 8 + 1)
        self.SetSizer(self.sizer)
        self.Show(True)

    def OnComposerClickEmoji(self, event):
        self.parent.clicked_composer_emoji = self.clicked_composer_emoji
        self.parent.OnComposerClickEmoji(event)

    def add_emojis_to_panel(self, category_list):
        self.realnum_emojis = 0
        for i in range(len(category_list)):
            emoji_string = category_list[i].lower()
            if '_skin_tone' in UNICODE_EMOJI[STRING_UNICODE[emoji_string]]:
                continue
            init_emoji = wx.Image(unicode_to_filename(STRING_UNICODE[emoji_string],
                                                      self.emoji_size))
            emoji = EmojiBitmap(wx.StaticBitmap(self, -1, wx.Bitmap(init_emoji)),
                                UNICODE_EMOJI[STRING_UNICODE[emoji_string]],
                                composer=self.composer, parent=self)
            self.sizer.Add(emoji.bitmap, 1, wx.ALIGN_CENTER)
            self.realnum_emojis += 1

    def add_most_used_emojis(self, category_list):
        self.realnum_emojis = 0
        for emoji in category_list:
            init_emoji = wx.Image(
                unicode_to_filename(emoji,
                                    self.emoji_size))
            emoji = EmojiBitmap(
                wx.StaticBitmap(self, -1, wx.Bitmap(init_emoji)),
                UNICODE_EMOJI[emoji],
                composer=self.composer, parent=self)
            self.sizer.Add(emoji.bitmap, 1, wx.ALIGN_LEFT)
            self.realnum_emojis += 1
