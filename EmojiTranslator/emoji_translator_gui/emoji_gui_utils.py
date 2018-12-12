import wx
from wx.adv import RichToolTip
from emoji_translator_utils.emoji_dict_utils import *

class EmojiSearchComboPopup(wx.ComboPopup):
    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.list_ctrl = None

    def AddItem(self, txt):
        self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), txt)

    def AddItems(self, items_list):
        for idx, item in enumerate(items_list):
            self.AddItem(item)

    def RemoveItems(self):
        self.list_ctrl.ClearAll()

    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.list_ctrl = wx.ListCtrl(parent,
                                     style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.list_ctrl.SetFont(wx.Font(25, wx.MODERN, wx.NORMAL, wx.NORMAL,
                                           False, u'Consolas'))
        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.list_ctrl

class EmojiBitmap(object):
    def __init__(self, bitmap, emoji_desc):
        self.bitmap = bitmap
        self.emoji_desc = emoji_desc.replace('_', ' ')
        self.bitmap.Bind(wx.EVT_RIGHT_DOWN,self.OnEmojiRightClick)

    def OnShowDesc(self, event):
        emoji_tip = wx.adv.RichToolTip(self.emoji_desc, "")
        emoji_tip.SetTitleFont(
            wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False,
                    u'Consolas'))
        emoji_tip.SetIcon(wx.Icon(self.resize_bitmap(16)))
        emoji_tip.ShowFor(self.bitmap)
        emoji_tip.SetTimeout(100)

    def OnCopyEmoji(self, event):
        dataObj = wx.TextDataObject()
        dataObj.SetText(EMOJI_UNICODE[self.emoji_desc.replace(' ', '_')])
        wx.TheClipboard.SetData(dataObj)
        wx.TheClipboard.Close()

    def OnEmojiRightClick(self, event):
        popupmenu = wx.Menu()
        popupmenu.Bind(wx.EVT_MENU, self.OnShowDesc,
                       popupmenu.Append(-1, 'Show Description'))
        popupmenu.Bind(wx.EVT_MENU, self.OnCopyEmoji,
                       popupmenu.Append(-1, 'Copy Emoji'))
        self.bitmap.PopupMenu(popupmenu)

    def resize_bitmap(self, size):
        image = self.bitmap.GetBitmap().ConvertToImage().Scale(size, size, wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)
