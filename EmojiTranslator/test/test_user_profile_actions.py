import unittest
from emoji_translator.main_app import *
from user_settings.settings import Settings

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.username = "test"
        self.profile_dir = "test_user_profiles"
        self.profile_path = os.path.join(os.getcwd(), self.profile_dir,
                                         self.username + ".pickle")
        self.test_profile = dict({
                "username" : self.username,
                "user_settings" : Settings(self.username),
                "saved_messages" : set(),
                "used_emojis": Counter()
        })

    def test_save_empty_user_profile(self):
        save_user_profile(self.username, self.test_profile, profile_dir=self.profile_dir)
        self.assertTrue(os.path.isfile(self.profile_path))

    def test_load_empty_user_profile(self):
        save_user_profile(self.username, self.test_profile,
                          profile_dir=self.profile_dir)
        profile = get_user_profile(self.username, profile_dir=self.profile_dir)
        self.assertEqual(profile, self.test_profile)

    def test_changed_user_profile(self):
        self.test_profile["username"] = "modified"
        self.username = self.test_profile["username"]
        self.test_profile["saved_messages"].add("this is a new message")
        self.test_profile["user_settings"].settings_dict[SettingsEnum.COMPOSER_TAB_FONT_SIZE] = 25
        save_user_profile(self.username, self.test_profile,
                          profile_dir=self.profile_dir)
        self.assertTrue(os.path.isfile(self.profile_path))
        profile = get_user_profile(self.username, profile_dir=self.profile_dir)
        self.assertEqual(profile, self.test_profile)

if __name__ == '__main__':
    unittest.main()