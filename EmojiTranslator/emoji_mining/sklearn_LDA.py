import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from emoji_mining.base_LDA import BaseLDA
import numpy

# manually labelled topics
TOPIC_LABELS_SK = {
    0 : "Sports",
    1 : "Film / Theatre",
    2 : "Education",
    3 : "Living",
    4 : "China",
    5 : "Geography - General",
    6 : "Transport - Cars / Aircrafts",
    7 : "Lifestyle",
    8 : "TV / Radio Shows - America",
    9 : "Literature",
    10 : "California / USA",
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
    21 : "Weather - Extreme",
    22 : "Science",
    23 : "England",
    24 : "Nature - Water",
    25 : "Books",
    26 : "Religion",
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
    38 : "Politics",
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

class SKLearnLDA(BaseLDA):
    def __init__(self):
        super().__init__()
        self.model = self.load_model()

    def predict_topic(self, text, best_k=2):
        tf = self.model.vectorizer.transform([text])
        topic_probability_scores = self.model.lda_model.transform(tf).tolist()[0]
        topic_probability_scores = [t for t in topic_probability_scores]

        best_k_topics = sorted(range(len(topic_probability_scores)), key=lambda i: topic_probability_scores[i])[-best_k:]
        best_k_topics.reverse()
        vocab = self.model.vectorizer.get_feature_names()

        topic_words = {}

        for topic, comp in enumerate(self.model.lda_model.components_):
            word_idx = numpy.argsort(comp)[::-1][:15]
            # store the words most relevant to the topic
            topic_words[topic] = [vocab[i] for i in word_idx]

        return [(TOPIC_LABELS_SK[topic], topic_probability_scores[topic]) for topic in best_k_topics]

    def create_model(self):
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000,
                                        stop_words='english')
        path = os.path.join(os.getcwd(), "../data", "docs_wiki.pkl")
        f = open(path, 'rb')
        documents = pickle.load(f)
        tf = tf_vectorizer.fit_transform(documents)
        lda = LatentDirichletAllocation(n_topics=50, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
        return ModelVectorizer(lda, tf_vectorizer)

    def save_model(self, model, dir_name="text_mining_models", file_name="sklearn_model.pickle"):
        if not os.path.exists(os.path.join(os.getcwd(), "..", dir_name)):
            os.makedirs(os.path.join(os.getcwd(), "..", dir_name))
        with open(os.path.join(os.getcwd(), "..", dir_name, file_name), "wb") as f:
            pickle.dump(model, f)

    def load_model(self, dir_name="text_mining_models", file_name="sklearn_model.pickle"):
        path = os.path.join(os.getcwd(), "..", dir_name, file_name)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                return pickle.load(f)
        else:
            model = self.create_model()
            self.save_model(model)
            return model

class ModelVectorizer(object):
    def __init__(self, model, vectorizer):
        self.lda_model = model
        self.vectorizer = vectorizer