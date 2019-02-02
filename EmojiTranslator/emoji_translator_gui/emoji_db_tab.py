import wx
from wx.lib.scrolledpanel import ScrolledPanel

from emoji_translator_utils.emoji_categ_parser import *
from emoji_translator_utils.emoji_dict_utils import *
from emoji_translator_gui.emoji_gui_utils import EmojiBitmap

class EmojiDBTab(ScrolledPanel):
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent)
        self.SetBackgroundColour((255, 253, 208))
        self.SetupScrolling(True)
        self.emoji_categories = emoji_categs_from_file()
        self.emoji_categ_buttons = dict()

        self.dbtab_sizer = wx.FlexGridSizer(3, 1, 0, 0)
        self.dbtab_sizer.AddGrowableRow(1)
        self.dbtab_sizer.AddGrowableCol(0)

        self.button_sizer = wx.GridSizer(1, len(self.emoji_categories), 0, 0)
        self.emoji_bmps_panel = wx.Panel()

        self.dbtab_sizer.Add(self.button_sizer, 1, wx.EXPAND)

        for cat in self.emoji_categories:
            bmp_path = unicode_to_filename(STRING_UNICODE[self.emoji_categories[cat][0]], 64)
            self.emoji_categ_buttons[cat] = wx.BitmapToggleButton(self, label=wx.Bitmap(bmp_path),
                                                                  name=cat, style=wx.BORDER_NONE)
            self.emoji_categ_buttons[cat].Bind(wx.EVT_TOGGLEBUTTON, self.OnEmojiCategory)
            self.emoji_categ_buttons[cat].SetBackgroundColour((255, 255, 255))
            self.button_sizer.Add(self.emoji_categ_buttons[cat], 1, wx.EXPAND)

        self.dbtab_sizer.AddSpacer(30)
        self.SetSizer(self.dbtab_sizer)

    def OnEmojiCategory(self, event):
        pressed_button = event.GetEventObject()
        pressed_button.SetBackgroundColour((105, 105, 105))
        for cat in self.emoji_categ_buttons:
            if not (self.emoji_categ_buttons[cat] is pressed_button):
                self.emoji_categ_buttons[cat].SetValue(False)
                self.emoji_categ_buttons[cat].SetBackgroundColour((255, 255, 255))

        self.populate_grid_with_emojis(pressed_button.GetName())
        self.SetupScrolling()
        self.Layout()

    def populate_grid_with_emojis(self, category):
        self.emoji_bmps_panel.Destroy()
        self.emoji_bmps_panel = EmojiPanel(self, self.emoji_categories[category])
        self.dbtab_sizer.Add(self.emoji_bmps_panel, 1, wx.EXPAND)

class EmojiPanel(wx.Panel):
    def __init__(self, parent, category_list):
        wx.Panel.__init__(self, parent)
        self.Show(False)
        self.sizer = wx.GridSizer(len(category_list) / 8 + 1, 8, 15, 0)
        self.emoji_size = 64
        self.add_emojis_to_panel(category_list)
        self.sizer.SetRows(self.realnum_emojis / 8 + 1)
        self.SetSizer(self.sizer)
        self.Show(True)

    def add_emojis_to_panel(self, category_list):
        self.realnum_emojis = 0
        for i in range(len(category_list)):
            emoji_string = category_list[i].lower()
            if '_skin_tone' in UNICODE_EMOJI[STRING_UNICODE[emoji_string]]:
                continue
            init_emoji = wx.Image(unicode_to_filename(STRING_UNICODE[emoji_string],
                                                      self.emoji_size))
            emoji = EmojiBitmap(wx.StaticBitmap(self, -1, wx.Bitmap(init_emoji)),
                                UNICODE_EMOJI[STRING_UNICODE[emoji_string]])

            self.sizer.Add(emoji.bitmap, 1, wx.ALIGN_CENTER)
            self.realnum_emojis += 1
