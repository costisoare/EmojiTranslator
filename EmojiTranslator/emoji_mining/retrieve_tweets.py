import tweepy
import csv
import os

def set_twitter_auth():
    auth = tweepy.OAuthHandler("kSvXU4RvL8SGJ0hIL7Q0SQihM",
                               "cIgz6WGDSwcE9Q1ZOj0CPv2R0B2IV3DSLoue34XEVcFRMUJg7H")
    auth.set_access_token("1106529638422073344-nESPkyqCZmHnxZvPdHgdoJPivYmo7G",
                          "ut66tGdedSTQ2nR9rK8w308ZRJ1LI6om62Nd4yEGTAgRQ")
    # Construct the API instance
    return tweepy.API(auth)

def read_csv_data():
    path = os.path.join(os.getcwd(), "../data", "Emojitracker_20150604.csv")
    emojis_by_occurrence = list()
    with open(path, encoding="utf8") as csvfile:
        file_data = csv.DictReader(csvfile)
        for row in file_data:
            emojis_by_occurrence.append(row["Emoji"])
    return emojis_by_occurrence

def get_tweets_by_emoji(api, emojis):
    tweets_by_emoji = dict()
    for emoji in emojis:
        tweets = tweepy.Cursor(api.search, q=emoji, lang="en").items(limit=100)
        tweets_by_emoji[emoji] = tweets
    return tweets_by_emoji