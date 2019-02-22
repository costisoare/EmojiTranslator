from emoji_translator_gui.enums import SettingsEnum

SETTINGS = dict({
    SettingsEnum.SEARCH_TAB_FONT_SIZE : 15,
    SettingsEnum.TRANSLATION_TAB_FONT_SIZE : 15,
    SettingsEnum.DB_EMOJI_SIZE : 64,
    SettingsEnum.COMPOSER_EMOJI_SIZE : 32,
    SettingsEnum.COMPOSER_TAB_FONT_SIZE : 15,
    SettingsEnum.TTS_SPEED : 120
})

GENERAL_SETTINGS = list([
    SettingsEnum.TTS_SPEED
])

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
    SettingsEnum.COMPOSER_EMOJI_SIZE,
    SettingsEnum.COMPOSER_TAB_FONT_SIZE
])