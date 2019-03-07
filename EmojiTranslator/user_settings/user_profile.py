from user_settings.settings import Settings
from collections import *

class OrderedCounter(Counter, OrderedDict):
    pass

class UserProfile(object):
    def __init__(self, username):
        self.username = username
        self.user_settings = Settings()
        self.saved_messages = set()
        self.used_emojis = OrderedCounter()

    def __eq__(self, other):
        return (self.username == other.username
                and self.user_settings == other.user_settings
                and self.saved_messages == other.saved_messages
                and self.used_emojis == other.used_emojis)