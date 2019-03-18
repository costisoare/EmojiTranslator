import tweepy
import csv
import os
import time
import pickle
from emoji_translator_utils.emoji_dict_utils import *

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

def save_tweets_by_emoji(api, emoji, data_dir="../twitter_emoji_data"):
    tweets_by_emoji = dict()
    try:
        profile_path = os.path.join(os.getcwd(), data_dir,
                                    UNICODE_EMOJI[emoji] + ".pickle")
        if not os.path.isfile(profile_path):
            tweets = tweepy.Cursor(api.search, q=emoji, lang="en").items(limit=100)
            tweets_by_emoji[emoji] = list()
            tweets_by_emoji[emoji] = retrieve_tweets(tweets)
    except KeyError:
        pass

def retrieve_tweets(tweets):
    text_tweets = list()
    while True:
        try:
            tweet = tweets.next()
            text_tweets.append(tweet.text)
        except tweepy.TweepError as e:
            print("====== WAIT ======")
            time.sleep(60 * 5)
            print("===== RESUME =====")
        except StopIteration:
            if len(text_tweets) < 100:
                print("INCOMPLETE: ", UNICODE_EMOJI[emoji], " ",
                      "MISSING: ",
                      str(100 - len(text_tweets)))
            save_emoji_tweets(emoji, text_tweets)
            return

def save_emoji_tweets(emoji, tweets, data_dir="../twitter_emoji_data"):
    profile_path = os.path.join(os.getcwd(), data_dir,
                                UNICODE_EMOJI[emoji] + ".pickle")
    if not os.path.exists(os.path.join(os.getcwd(), data_dir)):
       os.makedirs(os.path.join(os.getcwd(), data_dir))
    with open(profile_path, 'wb') as f:
        pickle.dump(tweets, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(UNICODE_EMOJI[emoji])

api = set_twitter_auth()
emojis = read_csv_data()

for emoji in emojis:
    save_tweets_by_emoji(api, emoji)