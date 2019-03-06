from emoji_translator_gui.emoji_gui_utils import *
from emoji_translator_utils.emoji_dict_utils import EMOJI_DESC_LIST
import difflib
import pyttsx3

class EmojiSearchTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.user_profile = self.parent.user_profile
        self.user_settings = self.parent.user_settings

        self.SetFont(wx.Font(self.user_settings.get_search_tab_font_size(), wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        self.SetBackgroundColour(self.user_settings.get_background_color())

        self.main_sizer = wx.GridSizer(2, 1, 0, 0)

        self.up_sizer = wx.FlexGridSizer(3, 1, 0, 0)
        self.up_sizer.AddGrowableCol(0)
        self.down_sizer = wx.GridSizer(1, 2, 0, 0)

        self.user_input = wx.ComboCtrl(self)
        self.user_input.SetHint("Search Emoji")
        self.user_input.SetPopupControl(EmojiComboPopup(self))
        self.user_input.GetPopupControl().GetControl().Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDescClick)
        self.user_input.Bind(wx.EVT_TEXT, self.OnInputChanged)

        self.up_sizer.AddSpacer(50)
        self.up_sizer.Add(self.user_input, 1, wx.EXPAND)

        self.tts_button = wx.Button(self, 0, "Text To Speech")
        self.tts_button.Bind(wx.EVT_BUTTON, self.OnTTS)
        self.tts_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.down_sizer.Add(self.tts_button, 1, wx.ALIGN_CENTER)
        self.tts_button.Show(False)

        self.main_sizer.Add(self.up_sizer, 1, wx.EXPAND)
        self.main_sizer.Add(self.down_sizer, 1, wx.EXPAND)

        self.SetSizer(self.main_sizer)

        self.tts_engine = pyttsx3.init()

    def OnInputChanged(self, event):
        matches = [match.replace("_", " ") for match in get_matched_list(self.user_input.GetValue())]
        self.user_input.GetPopupControl().RemoveItems()
        self.user_input.GetPopupControl().AddItems(matches)

    def OnDescClick(self, event):
        if self.user_profile["username"] != "guest":
            try:
                self.user_profile["used_emojis"].update([EMOJI_UNICODE[event.GetText()]])
            except KeyError:
                self.user_profile["used_emojis"].update([EMOJI_ALIAS_UNICODE[event.GetText()]])

        desc = event.GetText().replace(" ", "_")

        if hasattr(self, "emoji_symbol"):
            self.emoji_symbol.bitmap.Destroy()
            del self.emoji_symbol

        try:
            init_emoji = wx.Image(unicode_to_filename(EMOJI_UNICODE[desc], 128))
        except KeyError:
            init_emoji = wx.Image(unicode_to_filename(EMOJI_ALIAS_UNICODE[desc], 128))

        self.emoji_symbol = EmojiBitmap(wx.StaticBitmap(self, -1, wx.Bitmap(init_emoji)), desc, parent=self)
        self.down_sizer.Add(self.emoji_symbol.bitmap, 1, wx.ALIGN_CENTER)

        self.tts_button.Show(hasattr(self, "emoji_symbol") or hasattr(self, "out_text"))

        # this was moved from the popup implementation so that it
        # does not overlap with the on click impl in this class
        # this statement ensures that the input text is shown consistently
        self.user_input.GetPopupControl().value = self.user_input.GetPopupControl().curitem
        self.user_input.Dismiss()

        self.Layout()

    def OnTTS(self, event):
        self.tts_engine.setProperty("rate", self.user_settings.get_tts_speed())
        self.tts_engine.say(self.emoji_symbol.emoji_desc)
        self.tts_engine.runAndWait()


def get_matched_list(input_str, cutoff=0.6, emoji_list=EMOJI_DESC_LIST):
    return sorted(difflib.get_close_matches(input_str, emoji_list, 9, cutoff=cutoff),
                  key=lambda x: difflib.SequenceMatcher(None, x, input_str).ratio(),
                  reverse=True)