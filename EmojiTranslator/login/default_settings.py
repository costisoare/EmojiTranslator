import wx
from emoji_translator_gui.enums import SettingsEnum

SETTINGS = dict({
    SettingsEnum.SEARCH_TAB_FONT_SIZE : 15,
    SettingsEnum.TRANSLATION_TAB_FONT_SIZE : 15,
    SettingsEnum.DB_EMOJI_SIZE : 64,
    SettingsEnum.COMPOSER_EMOJI_SIZE : 32
})

SEARCH_SETTINGS = list([
    SettingsEnum.SEARCH_TAB_FONT_SIZE
])

TRANSLATE_SETTINGS = list([
    SettingsEnum.TRANSLATION_TAB_FONT_SIZE
])

DB_SETTINGS = list([
    SettingsEnum.DB_EMOJI_SIZE
])

COMPOSE_SETTINGS = list([
    SettingsEnum.COMPOSER_EMOJI_SIZE
])