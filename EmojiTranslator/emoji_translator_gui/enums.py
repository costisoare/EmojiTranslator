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