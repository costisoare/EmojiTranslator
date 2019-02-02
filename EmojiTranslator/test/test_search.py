import unittest
from emoji_translator_gui.emoji_search_tab import get_matched_list

class TestSearch(unittest.TestCase):
    def test_desc_in_list_notypo(self):
        cat_list = get_matched_list("cat")
        self.assertTrue("cat" in set(cat_list))

    def test_desc_in_list_withtypo(self):
        cat_list_with_type = get_matched_list("cst")
        self.assertTrue("cat" in set(cat_list_with_type))

    def test_desc_notin_list(self):
        no_cat_list = get_matched_list("bde")
        self.assertFalse("cat" in set(no_cat_list))

if __name__ == '__main__':
    unittest.main()