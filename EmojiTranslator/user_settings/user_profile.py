from user_settings.settings import Settings
from collections import *

LATEST_VERSION = "1.0"

VERSION_PROFILE_ATTRS = {
    "1.0" : {"version", "username", "user_settings", "saved_messages", "used_emojis"}
}

# to be updated once new attributes are introduced
# in a version later than 1.0
NEW_ATTR_INIT_TYPE = {
}

class OrderedCounter(Counter, OrderedDict):
    pass

class UserProfile(object):
    def __init__(self, username):
        self.version = LATEST_VERSION
        self.username = username
        self.user_settings = Settings()
        self.saved_messages = set()
        self.used_emojis = OrderedCounter()

    def __eq__(self, other):
        return (self.username == other.username
                and self.user_settings == other.user_settings
                and self.saved_messages == other.saved_messages
                and self.used_emojis == other.used_emojis)

def create_profile_from_existing(profile):
    current_attrs = VERSION_PROFILE_ATTRS[profile.version]
    new_attrs = VERSION_PROFILE_ATTRS[LATEST_VERSION].difference(current_attrs)

    # this will be updated once a new version is released
    for attr in new_attrs:
        setattr(profile, attr, NEW_ATTR_INIT_TYPE[attr])

    return profile