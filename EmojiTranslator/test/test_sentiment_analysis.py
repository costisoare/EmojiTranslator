import unittest
from emoji_mining.sentiment_analysis import *

class TestSentimentAnalysis(unittest.TestCase):
    def test_sent_rating(self):
        self.assertEqual("very positive", sent_rating(0.75, 0.75)[0])
        self.assertEqual("positive", sent_rating(0.35, 0.45)[0])
        self.assertEqual("neutral", sent_rating(0.01, -0.02)[0])
        self.assertEqual("negative", sent_rating(-0.35, -0.45)[0])
        self.assertEqual("very negative", sent_rating(-0.75, -0.75)[0])

    def test_end_to_end(self):
        self.assertEqual("very positive", emoji_sentiments_from_text("I love 🍌").get("🍌")[0])

if __name__ == '__main__':
    unittest.main()