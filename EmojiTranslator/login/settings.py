from login.default_settings import SETTINGS
from emoji_translator_gui.enums import SettingsEnum

class Settings(object):
    def __init__(self, username="guest"):
        self.username = username
        self.settings_dict = self.get_default_settings()

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