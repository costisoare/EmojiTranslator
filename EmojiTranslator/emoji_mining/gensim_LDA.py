import gensim
import gensim.corpora as corpora
import gensim.utils as utils
import re
import os
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from emoji_mining.base_LDA import BaseLDA
from gensim.models.ldamodel import LdaModel

TOPIC_LABELS_GENSIM = {
    0 : "Weather - Extreme / Ocean",
    1 : "France - Geography",
    2 : "Music - America",
    3 : "English Royals",
    4 : "Space",
    5 : "Books",
    6 : "Life Events",
    7 : "Cities",
    8 : "Nature - Climatology",
    9 : "Energy - Cars",
    10 : "American Actor",
    11 : "Education",
    12 : "Medicine",
    13 : "Ancient History",
    14 : "Transport - Air",
    15 : "People",
    16 : "Geography",
    17 : "Movies",
    18 : "Hockey",
    19 : "Spain",
    20 : "Australia - Sports",
    21 : "Transport - Navy / Air",
    22 : "USA - Geography",
    23 : "Chemistry",
    24 : "Biology",
    25 : "Politics",
    26 : "Movie Awards",
    27 : "Plants",
    28 : "Articles",
    29 : "Data / Files",
    30 : "Russia",
    31 : "Transport - Railway",
    32 : "People",
    33 : "Music - Rock",
    34 : "Olympic Games",
    35 : "Languages",
    36 : "Video Games",
    37 : "Sports - Football",
    38 : "USA",
    39 : "Time",
    40 : "Art - Painting",
    41 : "Nature",
    42 : "Computers",
    43 : "Media - TV / Radio",
    44 : "Sports - Basketball",
    45 : "India - History",
    46 : "Wars",
    47 : "Demographics",
    48 : "International Relations",
    49 : "Religion - Christianity",
}

class GensimLDA(BaseLDA):
    def __init__(self):
        super().__init__()
        self.model = self.load_model()

    def predict_topic(self, text, best_k=2):
        words = utils.simple_preprocess(str(text), deacc=True)
        stop_words = stopwords.words('english')
        lemmatizer = WordNetLemmatizer()

        data_lemmatized = list()

        data_lemmatized.append([lemmatizer.lemmatize(w) for w in words if w not in stop_words])
        id2word = corpora.Dictionary(data_lemmatized)
        texts = data_lemmatized
        corpus = [id2word.doc2bow(text) for text in texts]

        unseen_doc = corpus[0]
        vector = sorted(self.model[unseen_doc], key=lambda x: x[1], reverse=True)

        return [(TOPIC_LABELS_GENSIM[topic[0]], topic[1]) for topic in vector][:best_k]

    def create_model(self):
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

    def save_model(self, model, dir_name="text_mining_models", file_name="gensim_model"):
        if not os.path.exists(os.path.join(os.getcwd(), "..", dir_name)):
            os.makedirs(os.path.join(os.getcwd(), "..", dir_name))
        model.save(os.path.join(os.getcwd(), "..", dir_name, file_name))

    def load_model(self, dir_name="text_mining_models", file_name="gensim_model"):
        path = os.path.join(os.getcwd(), "..", dir_name, file_name)
        if os.path.isfile(path):
            return LdaModel.load(path)
        else:
            model = self.create_model()
            self.save_model()
            return model