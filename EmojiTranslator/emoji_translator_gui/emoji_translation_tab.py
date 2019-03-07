import wx
import emoji
import pyttsx3
import os
from emoji_translator_utils.emoji_dict_utils import *
from emoji_translator_utils.enums import *

class EmojiTranslationTab(wx.Panel):
    def __init__(self, parent, saved_text="", translation_direction=TranslationDirection.FROM_EMOJI_TO_TEXT):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.user_settings = self.parent.user_settings

        self.SetFont(wx.Font(self.user_settings.get_translation_tab_font_size(), wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.SetBackgroundColour(self.user_settings.get_background_color())

        self.parent = parent

        self.main_sizer = wx.FlexGridSizer(5, 1, 0, 0)

        self.main_sizer.AddGrowableRow(1)
        self.main_sizer.AddGrowableRow(4)
        self.main_sizer.AddGrowableCol(0)

        if translation_direction == TranslationDirection.FROM_EMOJI_TO_TEXT:
            self.translate_from = wx.StaticText(self, label="Text With Emojis")
            self.translate_to = wx.StaticText(self, label="Text Without Emojis")
        else:
            self.translate_from = wx.StaticText(self, label="Text Without Emojis")
            self.translate_to = wx.StaticText(self, label="Text With Emojis")

        self.translation_direction = translation_direction

        self.out_text = wx.TextCtrl(self, style=wx.TE_READONLY | wx.NO_BORDER | wx.TE_MULTILINE)
        self.out_text.SetBackgroundColour(self.GetBackgroundColour())

        self.user_input = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.user_input.Bind(wx.EVT_TEXT, self.OnInputChanged)
        self.user_input.SetValue(saved_text)

        swap_bmp_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'gui_utils_files', 'swap.png')
        swap_bmp = wx.Bitmap(swap_bmp_file).ConvertToImage()
        swap_bmp = swap_bmp.Scale(32, 32, wx.IMAGE_QUALITY_HIGH)
        swap_bmp = swap_bmp.Rotate90()
        self.swap_button = wx.BitmapButton(self, bitmap=wx.Bitmap(swap_bmp), style=wx.BORDER_NONE)
        self.swap_button.Bind(wx.EVT_BUTTON, self.OnSwapTranslate)
        self.swap_button.Bind(wx.EVT_MOTION, self.OnInputChanged)
        self.swap_button.SetBackgroundColour(self.GetBackgroundColour())
        self.swap_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        self.tts_button = wx.Button(self, label="Text To Speech")
        self.tts_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.tts_button.Bind(wx.EVT_BUTTON, self.OnTTS)

        middle_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        middle_buttons_sizer.Add(self.swap_button, 1, wx.ALIGN_CENTER)
        middle_buttons_sizer.Add(self.tts_button, 1, wx.ALIGN_RIGHT)

        self.main_sizer.Add(self.translate_from, 1, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)
        self.main_sizer.Add(self.user_input, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)
        self.main_sizer.Add(middle_buttons_sizer, 1, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)
        self.main_sizer.Add(self.translate_to, 1, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.RIGHT, 10)
        self.main_sizer.Add(self.out_text, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.RIGHT, 10)

        self.SetSizer(self.main_sizer)

        self.tts_engine = pyttsx3.init()

    def OnInputChanged(self, event):
        if self.translation_direction == TranslationDirection.FROM_EMOJI_TO_TEXT:
            self.out_text.SetValue(emoji.demojize(self.user_input.GetValue()))
        else:
            self.out_text.SetValue(emoji.emojize(self.user_input.GetValue(), use_aliases=True))

    def OnSwapTranslate(self, event):
        from_label = self.translate_from.GetLabel()
        to_label = self.translate_to.GetLabel()
        self.translate_from.SetLabel(to_label)
        self.translate_to.SetLabel(from_label)
        if self.translation_direction == TranslationDirection.FROM_TEXT_TO_EMOJI:
            self.translation_direction = TranslationDirection.FROM_EMOJI_TO_TEXT
        else:
            self.translation_direction = TranslationDirection.FROM_TEXT_TO_EMOJI

    def OnTTS(self, event):
        self.tts_engine.setProperty("rate", self.user_settings.get_tts_speed())
        self.tts_engine.say(tts_friendly_descriptions(self.out_text.GetValue()))
        self.tts_engine.runAndWait()
