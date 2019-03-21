import enum

class Tab(enum.Enum):
    SEARCH = "Search"
    DATABASE = "Database"
    TRANSLATE = "Translate"
    COMPOSE = "Compose"
    SETTINGS = "Settings"
    HELP = "Help"

class TranslationDirection(enum.Enum):
    FROM_TEXT_TO_EMOJI = 0
    FROM_EMOJI_TO_TEXT = 1

class SettingsEnum(enum.Enum):
    DB_EMOJI_SIZE = "DB Emoji Size"
    COMPOSER_EMOJI_SIZE = "Composer Emoji Size"
    SEARCH_TAB_FONT_SIZE = "Search Tab Font Size"
    TRANSLATION_TAB_FONT_SIZE = "Translation Tab Font Size"
    COMPOSER_TAB_FONT_SIZE = "Composer Tab Font Size"
    TTS_SPEED = "TTS Speed"
    BACKGROUND_COLOR = "Background Color"
    GENERAL_FONT_SIZE = "General Font Size"
    GENERAL_FONT_SIZE_ENABLED = "General Font Size Enabled"

class Sentiment(enum.Enum):
    VERY_POSITIVE = "very positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very negative"