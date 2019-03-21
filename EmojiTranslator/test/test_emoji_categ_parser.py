import unittest
from emoji_translator_utils.emoji_categ_parser import *

class TestEmojiCategParser(unittest.TestCase):
    def setUp(self):
        self.categories = emoji_categs_from_file()

    def test_parsed_categories(self):
        categs = ["-group:-smileys-&-people", "-group:-animals-&-nature", "-group:-food-&-drink", "-group:-travel-&-places",
                  "-group:-activities", "-group:-objects", "-group:-symbols", "-group:-flags"]
        self.assertEqual(categs, list(self.categories.keys()))

    def test_categ_has_emojis(self):
        for categ in self.categories:
            self.assertTrue(len(self.categories[categ]) > 0)

if __name__ == '__main__':
    unittest.main()