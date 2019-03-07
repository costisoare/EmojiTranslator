import wx
import pyttsx3
import speech_recognition as sr
import threading
from emoji_translator_gui.emoji_db_tab import EmojiDBTab
from emoji_translator_utils.emoji_dict_utils import *
from emoji_translator_gui.emoji_search_tab import get_matched_list
from emoji_translator_gui.emoji_gui_utils import *

class EmojiComposeTab(wx.Panel):
    def __init__(self, parent, saved_text=""):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.user_settings = self.parent.user_settings

        self.SetFont(wx.Font(self.user_settings.get_composer_tab_font_size(), wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self.user_profile = self.parent.user_profile

        self.SetBackgroundColour(self.user_settings.get_background_color())
        if self.user_profile.username == "guest":
            self.compose_tab_sizer = wx.FlexGridSizer(5, 1, 0, 0)
        else:
            self.compose_tab_sizer = wx.FlexGridSizer(7, 1, 0, 0)

        self.compose_tab_sizer.AddGrowableRow(0, proportion=1)
        self.compose_tab_sizer.AddGrowableRow(1, proportion=1)
        if self.user_profile.username == "guest":
            self.compose_tab_sizer.AddGrowableRow(2, proportion=15)
            self.compose_tab_sizer.AddGrowableRow(3, proportion=1)
            self.compose_tab_sizer.AddGrowableRow(4, proportion=15)
        else:
            self.compose_tab_sizer.AddGrowableRow(2, proportion=1)
            self.compose_tab_sizer.AddGrowableRow(3, proportion=15)
            self.compose_tab_sizer.AddGrowableRow(4, proportion=1)
            self.compose_tab_sizer.AddGrowableRow(5, proportion=1)
            self.compose_tab_sizer.AddGrowableRow(6, proportion=15)
        self.compose_tab_sizer.AddGrowableCol(0)

        self.top_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.tts_button = wx.Button(self, label="Text To Speech")
        self.tts_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.tts_button.Bind(wx.EVT_BUTTON, self.OnTTS)

        self.stt_button = wx.Button(self, label="Speech To Text")
        self.stt_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.stt_button.Bind(wx.EVT_BUTTON, self.OnSTT)

        self.top_buttons_sizer.Add(self.tts_button, 1, wx.ALIGN_CENTER)
        self.top_buttons_sizer.Add(self.stt_button, 1, wx.ALIGN_CENTER)

        self.editor = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.editor.SetValue(saved_text)
        self.emojis_tab = EmojiDBTab(self, composer=True)

        self.stt_result = wx.StaticText(self)

        # this is only used if a user is logged in
        self.save_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.save_button = wx.Button(self, label="Save Text")
        self.save_button.Bind(wx.EVT_BUTTON, self.OnSave)
        self.save_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.save_response = wx.StaticText(self)
        self.save_sizer.Add(self.save_button, 1, wx.ALIGN_CENTER)
        self.save_sizer.AddSpacer(20)
        self.save_sizer.Add(self.save_response, 1, wx.ALIGN_CENTER)

        # 3 autocomplete options
        self.auto_complete_options = wx.BoxSizer(wx.HORIZONTAL)

        self.auto_comp_opt1 = wx.Button(self, style=wx.BORDER_NONE|wx.BU_EXACTFIT)
        self.auto_comp_opt1.Bind(wx.EVT_BUTTON, self.OnPressAutoCorrect)
        self.auto_comp_opt1.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, True, u'Consolas'))
        self.auto_comp_opt1.SetBackgroundColour(self.GetBackgroundColour())
        self.auto_comp_opt1.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.auto_complete_options.Add(self.auto_comp_opt1, 1, wx.ALIGN_CENTER)
        self.auto_complete_options.AddSpacer(20)

        self.auto_comp_opt2 = wx.Button(self, style=wx.BORDER_NONE|wx.BU_EXACTFIT)
        self.auto_comp_opt2.Bind(wx.EVT_BUTTON, self.OnPressAutoCorrect)
        self.auto_comp_opt2.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, True, u'Consolas'))
        self.auto_comp_opt2.SetBackgroundColour(self.GetBackgroundColour())
        self.auto_comp_opt2.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.auto_complete_options.Add(self.auto_comp_opt2, 1, wx.ALIGN_CENTER)
        self.auto_complete_options.AddSpacer(20)

        self.auto_comp_opt3 = wx.Button(self, style=wx.BORDER_NONE|wx.BU_EXACTFIT)
        self.auto_comp_opt3.Bind(wx.EVT_BUTTON, self.OnPressAutoCorrect)
        self.auto_comp_opt3.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, True, u'Consolas'))
        self.auto_comp_opt3.SetBackgroundColour(self.GetBackgroundColour())
        self.auto_comp_opt3.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.auto_complete_options.Add(self.auto_comp_opt3, 1, wx.ALIGN_CENTER)

        self.saved_texts_options = wx.ComboCtrl(self)
        self.saved_texts_options.SetHint("Search Message")
        self.saved_texts_options.SetPopupControl(EmojiComboPopup(self))
        self.saved_texts_options.GetPopupControl().GetControl().Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnSavedTextClick)
        self.saved_texts_options.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.OnSavedTextSelection)

        self.compose_tab_sizer.Add(self.top_buttons_sizer, 1, wx.EXPAND)
        self.compose_tab_sizer.Add(self.stt_result, 1, wx.EXPAND)
        if self.user_profile.username != "guest":
            self.compose_tab_sizer.Add(self.saved_texts_options, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        else:
            self.saved_texts_options.Hide()
        self.compose_tab_sizer.Add(self.editor, 1, wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)

        if self.user_profile.username != "guest":
            self.compose_tab_sizer.Add(self.save_sizer, 1, wx.ALIGN_CENTER)
        else:
            self.save_button.Hide()

        self.compose_tab_sizer.Add(self.auto_complete_options, 1, wx.ALIGN_CENTER)
        self.compose_tab_sizer.Add(self.emojis_tab, 1, wx.EXPAND)

        self.editor.Bind(wx.EVT_TEXT, self.OnInputChanged)

        self.SetSizer(self.compose_tab_sizer)

        self.tts_engine = pyttsx3.init()

        self.Layout()

    def OnComposerClickEmoji(self, event):
        unicode = EMOJI_UNICODE[self.clicked_composer_emoji.replace(' ', '_')]
        self.user_profile.used_emojis.update([unicode])
        self.editor.AppendText(unicode)

    def OnInputChanged(self, event):
        text = self.editor.GetValue()
        emoji_descs = regex.findall(
            u'(%s[a-zA-Z0-9\+\-_&.ô’Åéãíç()!#*]+)' % ":",
            text)
        self.auto_comp_opt1.SetLabel("")
        self.auto_comp_opt1.Hide()
        self.auto_comp_opt2.SetLabel("")
        self.auto_comp_opt2.Hide()
        self.auto_comp_opt3.SetLabel("")
        self.auto_comp_opt3.Hide()
        if len(emoji_descs) > 0 and len(emoji_descs[-1]) > 2:
            to_autocomplete = emoji_descs[-1].replace(":", "")
            matches = get_matched_list(to_autocomplete, emoji_list=EMOJI_DESC_LIST)
            if len(matches) > 0:
                self.auto_comp_opt1.SetLabel(matches[0])
                self.auto_comp_opt1.Show()
            if len(matches) > 1:
                self.auto_comp_opt2.SetLabel(matches[1])
                self.auto_comp_opt2.Show()
            if len(matches) > 2:
                self.auto_comp_opt3.SetLabel(matches[2])
                self.auto_comp_opt3.Show()

        current_insertion_point = self.editor.GetInsertionPoint()
        new_text = emojize(self.editor.GetValue(), use_aliases=True)
        if new_text != self.editor.GetValue():
            self.auto_comp_opt1.SetLabel("")
            self.auto_comp_opt1.Hide()
            self.auto_comp_opt2.SetLabel("")
            self.auto_comp_opt2.Hide()
            self.auto_comp_opt3.SetLabel("")
            self.auto_comp_opt3.Hide()
        self.editor.ChangeValue(new_text)
        self.editor.SetInsertionPoint(current_insertion_point)
        self.Layout()

    def OnTTS(self, event):
        self.tts_engine.setProperty("rate", self.user_settings.get_tts_speed())
        self.tts_engine.say(tts_friendly_descriptions(self.editor.GetValue()))
        self.tts_engine.runAndWait()

    def OnSTT(self, event):
        self.stt_button.Disable()
        ListeningThread(self).start()

    def OnSave(self, event):
        self.save_response.SetLabel("")
        init_size = len(self.user_profile.saved_messages)
        try:
            text = self.editor.GetValue()
            if text != "":
                self.user_profile.saved_messages.add(text)
                if init_size != len(self.user_profile.saved_messages):
                    self.update_used_emojis_from_message(text)
                    self.save_response.SetLabel("Message has been saved!")
                else:
                    self.save_response.SetLabel("Message already exists!")
            else:
                self.save_response.SetLabel("Please input a message.")
        except:
            self.save_response.SetLabel("Message could not be saved...")

    def OnPressAutoCorrect(self, event):
        text = self.editor.GetValue()
        to_replace = regex.findall(
            u'(%s[a-zA-Z0-9\+\-_&.ô’Åéãíç()!#*]+)' % ":",
            text)[-1]
        self.editor.SetValue(self.editor.GetValue().replace(to_replace, ":" + event.GetEventObject().GetLabel() + ":"))
        self.auto_comp_opt1.Hide()
        self.auto_comp_opt2.Hide()
        self.auto_comp_opt3.Hide()
        self.Layout()

    def OnSavedTextSelection(self, event):
        input_val = self.saved_texts_options.GetValue()
        matches = [msg for msg in list(self.user_profile.saved_messages) if msg.startswith(input_val)]
        self.saved_texts_options.GetPopupControl().RemoveItems()
        self.saved_texts_options.GetPopupControl().AddItems(matches)
        self.Layout()

    def OnSavedTextClick(self, event):
        self.editor.AppendText(event.GetText())
        self.saved_texts_options.Dismiss()
        self.Layout()

    def update_used_emojis_from_message(self, text):
        emojis_in_message = []
        all_emoji_desc = regex.findall(
            u'(%s[a-zA-Z0-9\+\-_&.ô’Åéãíç()!#*]+%s)' % (":", ":"),
            demojize(text)
        )
        for desc in all_emoji_desc:
            parsed = desc[1:-1]
            if parsed in set(EMOJI_DESC_LIST):
                try:
                    emojis_in_message.append(EMOJI_UNICODE[parsed])
                except KeyError:
                    emojis_in_message.append(EMOJI_ALIAS_UNICODE[parsed])
        self.user_profile.used_emojis.update(emojis_in_message)


class ListeningThread(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent

    def run(self):
        self.parent.parent.search_button.Disable()
        self.parent.parent.db_button.Disable()
        self.parent.parent.composer_button.Disable()
        self.parent.parent.translate_button.Disable()
        self.parent.parent.settings_button.Disable()
        try:
            matched = self.recognize_emoji()
            if len(matched) > 0:
                self.parent.stt_result.SetLabel("Found: " + matched[0])
                try:
                    emoji = EMOJI_UNICODE[matched[0]]
                    self.parent.user_profile.used_emojis.update([emoji])
                    self.parent.editor.AppendText(emoji)
                except KeyError:
                    self.parent.editor.AppendText(EMOJI_ALIAS_UNICODE[matched[0]])
            else:
                self.parent.stt_result.SetLabel("Nothing found.")

            self.parent.stt_button.Enable()
        except sr.UnknownValueError:
            self.parent.stt_result.SetLabel("Nothing found.")
            self.parent.stt_button.Enable()
        finally:
            self.parent.parent.search_button.Enable()
            self.parent.parent.db_button.Enable()
            self.parent.parent.composer_button.Enable()
            self.parent.parent.translate_button.Enable()
            self.parent.parent.settings_button.Enable()

    def recognize_emoji(self):
        r = sr.Recognizer()
        self.parent.stt_result.SetLabel("Microphone setup...")
        mic = sr.Microphone()
        with mic as source:
            self.parent.stt_result.SetLabel("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source)
            self.parent.stt_result.SetLabel("Listening...")
            audio = r.listen(source, phrase_time_limit=5)

        self.parent.stt_result.SetLabel("Translating into emoji...")
        recognized_str = r.recognize_bing(audio, key="7bdc27c1138e48b59c255595b5102c4f")
        #recognized_str = r.recognize_sphinx(audio)

        string_to_search = recognized_str.replace(".", "").lower()
        return get_matched_list(string_to_search)


