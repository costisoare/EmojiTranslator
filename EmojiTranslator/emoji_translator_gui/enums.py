import enum

class Tab(enum.Enum):
    SEARCH = "Search"
    DATABASE = "Database"
    TRANSLATE = "Translate"
    COMPOSE = "Compose"
    SETTINGS = "Settings"

class TranslationDirection(enum.Enum):
    FROM_TEXT_TO_EMOJI = 0
    FROM_EMOJI_TO_TEXT = 1

class SettingsEnum(enum.Enum):
    DB_EMOJI_SIZE = "db_emoji_size"
    COMPOSER_EMOJI_SIZE = "composer_emoji_size"
    SEARCH_TAB_FONT_SIZE = "search_tab_font_size"
    TRANSLATION_TAB_FONT_SIZE = "translation_tab_font_size"