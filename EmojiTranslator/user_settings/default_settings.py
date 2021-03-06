from emoji_translator_utils.enums import SettingsEnum

SETTINGS = dict({
    SettingsEnum.SEARCH_TAB_FONT_SIZE : 15,
    SettingsEnum.TRANSLATION_TAB_FONT_SIZE : 15,
    SettingsEnum.DB_EMOJI_SIZE : 64,
    SettingsEnum.COMPOSER_EMOJI_SIZE : 32,
    SettingsEnum.COMPOSER_TAB_FONT_SIZE : 15,
    SettingsEnum.TTS_SPEED : 120,
    SettingsEnum.BACKGROUND_COLOR : (255, 253, 208),
    SettingsEnum.GENERAL_FONT_SIZE : 15,
    SettingsEnum.GENERAL_FONT_SIZE_ENABLED : False,
    SettingsEnum.TEXT_MINING_MODEL: "sklearn"
})

GENERAL_SETTINGS = list([
    SettingsEnum.GENERAL_FONT_SIZE,
    SettingsEnum.GENERAL_FONT_SIZE_ENABLED,
    SettingsEnum.TTS_SPEED,
    SettingsEnum.BACKGROUND_COLOR,
    SettingsEnum.TEXT_MINING_MODEL
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