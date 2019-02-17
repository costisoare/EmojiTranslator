import wx
import regex
import pyttsx3
from emoji_translator_gui.emoji_db_tab import EmojiDBTab
from emoji_translator_utils.emoji_dict_utils import *

class EmojiComposeTab(wx.Panel):
    def __init__(self, parent, saved_text=""):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour((255, 253, 208))
        self.readable_editor_text = ""
        self.compose_tab_sizer = wx.FlexGridSizer(3, 1, 0, 0)

        self.compose_tab_sizer.AddGrowableRow(0, proportion=1)
        self.compose_tab_sizer.AddGrowableRow(1, proportion=10)
        self.compose_tab_sizer.AddGrowableRow(2, proportion=10)
        self.compose_tab_sizer.AddGrowableCol(0)

        self.tts_button = wx.Button(self, label="Text To Speech")
        self.tts_button.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.tts_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.tts_button.Bind(wx.EVT_BUTTON, self.OnTTS)

        self.editor = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.editor.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.editor.SetValue(saved_text)
        self.emojis_tab = EmojiDBTab(self, composer=True)

        self.compose_tab_sizer.Add(self.tts_button, 1, wx.EXPAND)
        self.compose_tab_sizer.Add(self.editor, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        self.compose_tab_sizer.Add(self.emojis_tab, 1, wx.EXPAND)

        self.editor.Bind(wx.EVT_TEXT, self.OnInputChanged)

        self.SetSizer(self.compose_tab_sizer)

        self.tts_engine = pyttsx3.init()

    def OnComposerClickEmoji(self, event):
        unicode = EMOJI_UNICODE[self.clicked_composer_emoji.replace(' ', '_')]
        self.editor.AppendText(unicode)

    def OnInputChanged(self, event):
        current_insertion_point = self.editor.GetInsertionPoint()
        self.editor.ChangeValue(emojize(self.editor.GetValue(), use_aliases=True))
        self.editor.SetInsertionPoint(current_insertion_point)

    def OnTTS(self, event):
        self.tts_engine.say(tts_friendly_descriptions(self.editor.GetValue()))
        self.tts_engine.runAndWait()