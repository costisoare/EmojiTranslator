from login.default_settings import SETTINGS
from emoji_translator_gui.enums import SettingsEnum

class Settings(object):
    def __init__(self, username="guest"):
        self.username = username
        self.settings_dict = self.get_default_settings()

    def __eq__(self, other):
        return (self.username == other.username and self.settings_dict == other.settings_dict)

    def __repr__(self):
        return str(self.settings_dict)

    def get_default_settings(self):
        return SETTINGS

    def get_user_settings(self, username):
        return SETTINGS

    def get_db_emoji_size(self):
        return self.settings_dict.get(SettingsEnum.DB_EMOJI_SIZE)

    def get_composer_emoji_size(self):
        return self.settings_dict.get(SettingsEnum.COMPOSER_EMOJI_SIZE)

    def get_search_tab_font_size(self):
        return self.settings_dict.get(SettingsEnum.SEARCH_TAB_FONT_SIZE)

    def get_translation_tab_font_size(self):
        return self.settings_dict.get(SettingsEnum.TRANSLATION_TAB_FONT_SIZE)

    def get_composer_tab_font_size(self):
        return self.settings_dict.get(SettingsEnum.COMPOSER_TAB_FONT_SIZE)

    def get_tts_speed(self):
        speed_str = self.settings_dict.get(SettingsEnum.TTS_SPEED)
        if speed_str == "slow":
            return 50
        elif speed_str == "fast":
            return 200
        else:
            return 125
