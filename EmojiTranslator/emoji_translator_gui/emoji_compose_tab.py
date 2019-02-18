import wx
import regex
import pyttsx3
import speech_recognition as sr
import threading
from emoji_translator_gui.emoji_db_tab import EmojiDBTab
from emoji_translator_utils.emoji_dict_utils import *
from emoji_translator_gui.emoji_search_tab import get_matched_list
from wx.adv import RichToolTip

class EmojiComposeTab(wx.Panel):
    def __init__(self, parent, saved_text=""):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour((255, 253, 208))
        self.compose_tab_sizer = wx.FlexGridSizer(4, 1, 0, 0)

        self.compose_tab_sizer.AddGrowableRow(0, proportion=1)
        self.compose_tab_sizer.AddGrowableRow(1, proportion=1)
        self.compose_tab_sizer.AddGrowableRow(2, proportion=15)
        self.compose_tab_sizer.AddGrowableRow(3, proportion=15)
        self.compose_tab_sizer.AddGrowableCol(0)

        self.top_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.tts_button = wx.Button(self, label="Text To Speech")
        self.tts_button.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.tts_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.tts_button.Bind(wx.EVT_BUTTON, self.OnTTS)

        self.stt_button = wx.Button(self, label="Speech To Text")
        self.stt_button.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.stt_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.stt_button.Bind(wx.EVT_BUTTON, self.OnSTT)

        self.top_buttons_sizer.Add(self.tts_button, 1, wx.ALIGN_CENTER)
        self.top_buttons_sizer.Add(self.stt_button, 1, wx.ALIGN_CENTER)

        self.editor = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.editor.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.editor.SetValue(saved_text)
        self.emojis_tab = EmojiDBTab(self, composer=True)

        self.stt_result = wx.StaticText(self)
        self.stt_result.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self.compose_tab_sizer.Add(self.top_buttons_sizer, 1, wx.EXPAND)
        self.compose_tab_sizer.Add(self.stt_result, 1, wx.EXPAND)
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

    def OnSTT(self, event):
        self.stt_button.Disable()
        ListeningThread(self).start()

class ListeningThread(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent

    def run(self):
        try:
            matched = recognize_emoji()
            if len(matched) > 0:
                self.parent.stt_result.SetLabel("Found: " + matched[0])
                try:
                    self.parent.editor.AppendText(EMOJI_UNICODE[matched[0]])
                except KeyError:
                    self.parent.editor.AppendText(EMOJI_ALIAS_UNICODE[matched[0]])
            else:
                self.parent.stt_result.SetLabel("Nothing found.")

            self.parent.stt_button.Enable()
        except sr.UnknownValueError:
            self.parent.stt_result.SetLabel("Nothing found.")
            self.parent.stt_button.Enable()

def recognize_emoji():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=5)

    recognized_str = r.recognize_bing(audio, key="7bdc27c1138e48b59c255595b5102c4f")
    #recognized_str = r.recognize_sphinx(audio)

    string_to_search = recognized_str.replace(".", "").lower()
    return get_matched_list(string_to_search)

