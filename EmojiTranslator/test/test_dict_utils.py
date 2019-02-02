import unittest
from emoji_translator_utils.emoji_dict_utils import *
import os

class TestDictUtils(unittest.TestCase):
    def test_simple_unicode_to_full_string(self):
        self.assertEqual("1f92d", unicode_to_fullstring(u'\U0001F92D'))

    def test_composed_unicode_to_full_string(self):
        self.assertEqual("270d-1f3ff", unicode_to_fullstring(u'\U0000270D\U0001F3FF'))

    def test_unicode_to_filename_simple(self):
        self.assertEqual(r"C:\Users\Costi\Desktop\Third Year Project\EmojiTranslator\emoji_translator_utils\../../EmojiOne_4.0_64x64_png/1f92d.thumbnail",
                         unicode_to_filename(u'\U0001F92D', 64))

    def test_unicode_to_filename_composed(self):
        self.assertEqual(r"C:\Users\Costi\Desktop\Third Year Project\EmojiTranslator\emoji_translator_utils\../../EmojiOne_4.0_64x64_png/270d-1f3ff.thumbnail",
                         unicode_to_filename(u'\U0000270D\U0001F3FF', 64))

    def test_unicode_to_filename_composed_with_ignored_part(self):
        self.assertEqual(r"C:\Users\Costi\Desktop\Third Year Project\EmojiTranslator\emoji_translator_utils\../../EmojiOne_4.0_128x128_png/1f471-2642.png",
                         unicode_to_filename(u'\U0001F471\U0000200D\U00002642\U0000FE0F', 128, "png"))

    def test_unicode_for_inexistent_file(self):
        self.assertEqual("FILE NOT FOUND", unicode_to_filename(u'\U00011111', 32))

if __name__ == '__main__':
    unittest.main()