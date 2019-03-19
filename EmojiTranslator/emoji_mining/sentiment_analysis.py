import csv
from nltk.sentiment.vader import *
from emoji_translator_utils.enums import Sentiment
from emoji_translator_utils.emoji_dict_utils import *

analyzer = SentimentIntensityAnalyzer()

def polarity_string(score):
    if score < -0.5:
        return Sentiment.VERY_NEGATIVE.value, 1
    elif score < -0.05:
        return Sentiment.NEGATIVE.value, 2
    elif score < 0.05:
        return Sentiment.NEUTRAL.value, 3
    elif score < 0.5:
        return Sentiment.POSITIVE.value, 4
    else:
        return Sentiment.VERY_POSITIVE.value, 5

def sent_rating(compound_score, emoji_sent_score=0):
    if emoji_sent_score is None:
        emoji_sent_score = 0
    diff = abs(polarity_string(emoji_sent_score)[1] - polarity_string(compound_score)[1])
    if diff >= 2:
        if abs(compound_score) > abs(emoji_sent_score):
            score = compound_score
        else:
            score = emoji_sent_score
    else:
        score = round((compound_score + emoji_sent_score) / 2, 3)

    return polarity_string(score)[0], score

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