import wx
from wx.lib.expando import ExpandoTextCtrl
import emoji
from emoji_translator_utils.emoji_dict_utils import *
import os

FROM_TEXT_TO_EMOJI = 0
FROM_EMOJI_TO_TEXT = 1

class EmojiTranslationTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.SetBackgroundColour((255, 253, 208))

        self.main_sizer = wx.FlexGridSizer(2, 3, 0, 0)

        self.main_sizer.AddGrowableRow(1)
        self.main_sizer.AddGrowableCol(0)
        self.main_sizer.AddGrowableCol(2)

        self.translate_from = wx.StaticText(self, label="Text With Emojis")
        self.translate_to = wx.StaticText(self, label="Text Without Emojis")
        self.translation_direction = FROM_EMOJI_TO_TEXT

        self.user_input = ExpandoTextCtrl(self)
        self.user_input.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.user_input.Bind(wx.EVT_TEXT, self.OnInputChanged)

        swap_bmp = wx.Bitmap(os.getcwd() + "\swap.png").ConvertToImage().Scale(32, 32, wx.IMAGE_QUALITY_HIGH)
        self.swap_button = wx.BitmapButton(self, bitmap=wx.Bitmap(swap_bmp), style=wx.BORDER_NONE)
        self.swap_button.Bind(wx.EVT_BUTTON, self.OnSwapTranslate)
        self.swap_button.Bind(wx.EVT_MOTION, self.OnSwapMouseMotion)
        self.swap_button.Bind(wx.EVT_MOTION, self.OnInputChanged)
        self.swap_button.SetBackgroundColour(self.GetBackgroundColour())

        self.out_text = ExpandoTextCtrl(self, style=wx.TE_READONLY|wx.NO_BORDER)
        self.out_text.SetBackgroundColour(self.GetBackgroundColour())
        self.out_text.SetFont(self.user_input.GetFont())

        self.main_sizer.Add(self.translate_from, 1, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        self.main_sizer.Add(self.swap_button, 1, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)
        self.main_sizer.Add(self.translate_to, 1, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.RIGHT, 10)
        self.main_sizer.Add(self.user_input, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        self.main_sizer.Add(wx.StaticText(self, label=""), 1, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)
        self.main_sizer.Add(self.out_text, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, 10)

        self.SetSizer(self.main_sizer)

        import pyttsx3
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', self.tts_engine.getProperty('rate') - 80)

    def OnInputChanged(self, event):
        if self.translation_direction == FROM_EMOJI_TO_TEXT:
            self.out_text.SetValue(emoji.demojize(self.user_input.GetValue()))
        else:
            self.out_text.SetValue(emoji.emojize(self.user_input.GetValue(), use_aliases=True))

    def OnTTS(self, event):
        if hasattr(self, "emoji_symbol"):
            self.tts_engine.say(self.emoji_symbol.emoji_desc)
        else:
            self.tts_engine.say(self.out_text.GetLabel())
        self.tts_engine.runAndWait()

    def OnSwapTranslate(self, event):
        from_label = self.translate_from.GetLabel()
        to_label = self.translate_to.GetLabel()
        self.translate_from.SetLabel(to_label)
        self.translate_to.SetLabel(from_label)
        self.translation_direction = not self.translation_direction

    def OnSwapMouseMotion(self, event):
        self.swap_button.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
