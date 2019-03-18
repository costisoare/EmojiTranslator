import csv
from nltk.sentiment.vader import *
from emoji_translator_utils.enums import Sentiment
from emoji_translator_utils.emoji_dict_utils import *

analyzer = SentimentIntensityAnalyzer()

def sent_rating(compound_score, emoji_sent_score=0):
    if emoji_sent_score is None:
        emoji_sent_score = 0
    score = round((compound_score + emoji_sent_score) / 2, 3)
    if score < -0.5:
        return Sentiment.VERY_NEGATIVE.value, score
    elif score < -0.05:
        return Sentiment.NEGATIVE.value, score
    elif score < 0.05:
        return Sentiment.NEUTRAL.value, score
    elif score < 0.5:
        return Sentiment.POSITIVE.value, score
    else:
        return Sentiment.VERY_POSITIVE.value, score

# get the csv data to compute emoji individual scores
def emoji_sentiment_scores():
    path = os.path.join(os.getcwd(), "../data", "Emoji_Sentiment_Data_v1.0.csv")
    emojis_with_score = dict()
    with open(path, encoding="utf8") as csvfile:
        file_data = csv.DictReader(csvfile)
        for row in file_data:
            emojis_with_score[row["Emoji"]] = round((float(row["Positive"])
                                               - float(row["Negative"])) / float(row["Occurrences"]), 3)
    return emojis_with_score

# return the final score of an emoji taking into account the text score as well
def emoji_sentiments_from_text(text=""):
    emoji_overall_score = dict()
    compound_score = float(analyzer.polarity_scores(text)["compound"])
    emojis = get_emojis_from_text(text)
    emoji_sent_scores = emoji_sentiment_scores()
    for emoji in emojis:
        emoji_overall_score[emoji] = sent_rating(compound_score, emoji_sent_scores.get(emoji))

    return emoji_overall_score