import wx
from wx.lib.scrolledpanel import ScrolledPanel

HELP_STRINGS = dict({
    "Search" : """
    * When searching, write your desired input into the search space.
    * Press the arrow on the right and you will be able to choose the option that best fits your desire.
    * Click on the choice to see more info about the chosen emoji.
            """,
    "Translation" : """
    * There are 2 "languages": with emojis and without emojis.
    * There is a "cheat": type an emoji description between : :, with words separated by an undescore (_), e.g. :thumbs_up:
    * Only valid descriptions will be taken into account, i.e. :thumbs up: or :thumbs: will not work.
            """,
    "Composer" : """
    * Very similar to the classic message composer with emojis: it has a text box and an emoji selection space.
    * The translation "cheat" works here, as well.
    * There is also an auto-complete option that gets activated when you start typing an emoji description. E.g. when you type ":ca", there will be auto-complete options, such as cat or car.
            """,
    "Miscellaneous" : """
    * Every emoji image (not inside the text fields) has 2 right click options: 
        - Copy Emoji - this enables the user to copy the emoji in any message composer, such as Twitter, Facebook etc.
        - Show Description - this opens a tooltip with the official text description and with the real size emoji.
            """
})

class EmojiHelpTab(ScrolledPanel):
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent)
        self.SetupScrolling(True, True)
        self.parent = parent
        self.user_profile = self.parent.user_profile
        self.user_settings = self.parent.user_settings

        self.SetBackgroundColour(self.user_settings.get_background_color())
        self.SetFont(wx.Font(self.user_settings.get_general_font_size() if self.user_settings.get_is_general_font_size_enabled() else 15,
            wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self.title_font = self.GetFont()
        self.title_font.SetUnderlined(True)

        self.help_labels = list()

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        for cat in HELP_STRINGS.keys():
            self.add_help(cat)

        self.SetSizer(self.sizer)
        self.Layout()

    def add_help(self, cat):
        sizer = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(self, label=cat)
        st.SetFont(self.title_font)
        sizer.Add(st)
        sizer.Add(self.get_text_cat(cat))
        self.sizer.Add(sizer)

    def get_text_cat(self, cat):
        st = wx.StaticText(self)
        st.SetLabel(HELP_STRINGS[cat])
        st.Wrap(self.parent.GetSize().GetWidth() - 170) # 170 is the ~width of the buttons panel
        self.help_labels.append(st)
        return st

