import wx
from wx.adv import RichToolTip
from emoji_translator_utils.emoji_dict_utils import *

class EmojiComboPopup(wx.ComboPopup):
    def __init__(self, parent):
        wx.ComboPopup.__init__(self)
        self.parent = parent
        self.list_ctrl = None

    def AddItem(self, txt):
        self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), txt)

    def AddItems(self, items_list):
        for idx, item in enumerate(items_list):
            self.AddItem(item)

    def RemoveItems(self):
        self.list_ctrl.ClearAll()

    def OnMotion(self, evt):
        item, flags = self.list_ctrl.HitTest(evt.GetPosition())
        if item >= 0:
            self.list_ctrl.Select(item)
            self.curitem = item

    # The following methods are those that are overridable from the
    # ComboPopup base class.
    def Init(self):
        self.value = -1
        self.curitem = -1

    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.list_ctrl = wx.ListCtrl(parent, style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.list_ctrl.Bind(wx.EVT_MOTION, self.OnMotion)
        self.list_ctrl.SetFont(self.parent.GetFont())
        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.list_ctrl

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, value):
        index = self.list_ctrl.FindItem(-1, value)
        if index != wx.NOT_FOUND:
            self.list_ctrl.Select(index)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.list_ctrl.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        wx.ComboPopup.OnDismiss(self)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.ComboPopup.OnComboKeyEvent(self, event)

    def OnComboDoubleClick(self):
        wx.ComboPopup.OnComboDoubleClick(self)

class EmojiBitmap(object):
    def __init__(self, bitmap, emoji_desc, composer=False, parent=None):
        self.parent = parent
        self.bitmap = bitmap
        self.emoji_desc = emoji_desc.replace('_', ' ')
        self.bitmap.Bind(wx.EVT_RIGHT_DOWN,self.OnEmojiRightClick)
        if composer:
            self.bitmap.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.bitmap.Bind(wx.EVT_LEFT_UP, self.OnComposerClickEmoji)

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
        try:
            dataObj.SetText(EMOJI_UNICODE[self.emoji_desc.replace(' ', '_')])
        except KeyError:
            dataObj.SetText(EMOJI_ALIAS_UNICODE[self.emoji_desc.replace(' ', '_')])
        wx.TheClipboard.SetData(dataObj)
        wx.TheClipboard.Close()

    def OnComposerClickEmoji(self, event):
        self.parent.clicked_composer_emoji = self.emoji_desc.replace(' ', '_')
        self.parent.OnComposerClickEmoji(event)

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