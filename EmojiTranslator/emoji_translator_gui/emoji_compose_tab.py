import wx
from emoji_translator_gui.emoji_db_tab import EmojiDBTab
from emoji_translator_utils.emoji_dict_utils import EMOJI_UNICODE, STRING_UNICODE
from emoji_translator_utils.emoji_dict_utils import unicode_to_filename
from wx.richtext import RichTextCtrl

class EmojiComposeTab(wx.Panel):
    def __init__(self, parent, saved_text=""):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour((255, 253, 208))
        self.readable_editor_text = ""
        self.compose_tab_sizer = wx.FlexGridSizer(2, 1, 0, 0)

        self.compose_tab_sizer.AddGrowableRow(0)
        self.compose_tab_sizer.AddGrowableRow(1)
        self.compose_tab_sizer.AddGrowableCol(0)

        self.editor = RichTextCtrl(self)
        self.editor.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.editor.SetValue(saved_text)
        self.emojis_tab = EmojiDBTab(self, composer=True)
        self.compose_tab_sizer.Add(self.editor, 1, wx.EXPAND)
        self.compose_tab_sizer.Add(self.emojis_tab, 1, wx.EXPAND)

        self.SetSizer(self.compose_tab_sizer)

    def OnComposerClickEmoji(self, event):
        unicode = EMOJI_UNICODE[self.clicked_composer_emoji.replace(' ', '_')]
        self.editor.AppendText(unicode)
        self.editor.AppendText(" ")