import gensim
import gensim.corpora as corpora
import re
import os
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

TOPIC_LABELS_GENSIM = {
    0 : "Sport",
    1 : "Film / Theatre",
    2 : "Education",
    3 : "Government - Living",
    4 : "China",
    5 : "Geography - General",
    6 : "Transport - Cars / Aircrafts",
    7 : "Lifestyle",
    8 : "TV/Radio Shows - America",
    9 : "Literature",
    10 : "California/  USA",
    11 : "London / UK",
    12 : "Music",
    13 : "New York Sports",
    14 : "Law / Politics",
    15 : "Ancient History / Greece",
    16 : "Baseball / USA",
    17 : "Olympic Games",
    18 : "France - Geography",
    19 : "Media / Gossip",
    20 : "Energy - Gas / Electricity",
    21 : "Weather - Economic Damage",
    22 : "Science - Research",
    23 : "England",
    24 : "Ocean Fish Trade",
    25 : "Books",
    26 : "Religion - Catholic Church",
    27 : "British History",
    28 : "War",
    29 : "Animals / Plants",
    30 : "USA - Geography",
    31 : "Hockey / Video Games",
    32 : "Movie Awards",
    33 : "Politics",
    34 : "Buildings",
    35 : "Basketball / American Sports",
    36 : "Russia - Geography",
    37 : "Wrestling",
    38 : "President - Politics",
    39 : "Wikipedia",
    40 : "Biology",
    41 : "Spain - History",
    42 : "Weather",
    43 : "Life Events",
    44 : "Computers",
    45 : "Languages",
    46 : "Astronomy",
    47 : "Transport / Railway",
    48 : "Art",
    49 : "Canada - Geography",
}

def predict_topic_gensim(text, model):
    words = gensim.utils.simple_preprocess(str(text), deacc=True)
    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()

    data_lemmatized = list()

    data_lemmatized.append([lemmatizer.lemmatize(w) for w in words if w not in stop_words])
    id2word = corpora.Dictionary(data_lemmatized)
    texts = data_lemmatized
    corpus = [id2word.doc2bow(text) for text in texts]

    unseen_doc = corpus[0]
    vector = sorted(model[unseen_doc], key=lambda x: x[1], reverse=True)
    for topic in model.show_topics(50, 10):
        print(topic)
    return [(TOPIC_LABELS_GENSIM[topic[0]], topic[1]) for topic in vector]

def create_model_gensim():
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

    path = os.path.join(os.getcwd(), "../data", "docs_wiki.pkl")
    f = open(path, 'rb')
    data = pickle.load(f)

    # Remove Emails
    data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]
    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]

    words = list()
    for sentence in data:
        words.append(gensim.utils.simple_preprocess(str(sentence), deacc=True))
    data_words = list(words)

    lemmatizer = WordNetLemmatizer()
    data_lemmatized = [[lemmatizer.lemmatize(w) for w in sent if w not in stop_words] for sent in data_words]

    id2word = corpora.Dictionary(data_lemmatized)
    texts = data_lemmatized
    corpus = [id2word.doc2bow(text) for text in texts]
    return gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=50)

def save_model_gensim(model, dir_name="text_mining_models", file_name="gensim_model"):
    if not os.path.exists(os.path.join(os.getcwd(), "..", dir_name)):
        os.makedirs(os.path.join(os.getcwd(), "..", dir_name))
    model.save(os.path.join(os.getcwd(), "..", dir_name, file_name))

def load_model_gensim(dir_name="text_mining_models", file_name="gensim_model"):
    path = os.path.join(os.getcwd(), "..", dir_name, file_name)
    if os.path.isfile(path):
        return gensim.models.ldamodel.LdaModel.load(path)
    else:
        model = create_model_gensim()
        save_model_gensim(model)
        return model

model = load_model_gensim()
predict_topic_gensim("religion", model)