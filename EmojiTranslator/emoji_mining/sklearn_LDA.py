import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy

class ModelVectorizer(object):
    def __init__(self, model, vectorizer):
        self.lda_model = model
        self.vectorizer = vectorizer

def predict_topic_sk(text, model):
    tf = model.vectorizer.transform([text])
    topic_probability_scores = model.lda_model.transform(tf).tolist()[0]
    best_topic = topic_probability_scores.index(max(topic_probability_scores))
    vocab = model.vectorizer.get_feature_names()

    topic_words = {}

    for topic, comp in enumerate(model.lda_model.components_):
        word_idx = numpy.argsort(comp)[::-1][:10]

        # store the words most relevant to the topic
        topic_words[topic] = [vocab[i] for i in word_idx]
    return topic_words[best_topic]

def create_model_sk():
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000,
                                    stop_words='english')
    path = os.path.join(os.getcwd(), "../data", "docs_wiki.pkl")
    f = open(path, 'rb')
    documents = pickle.load(f)
    tf = tf_vectorizer.fit_transform(documents)
    lda = LatentDirichletAllocation(n_topics=50, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    return ModelVectorizer(lda, tf_vectorizer)

def save_model_sk(model, dir_name="text_mining_models", file_name="sklearn_model.pickle"):
    if not os.path.exists(os.path.join(os.getcwd(), "..", dir_name)):
        os.makedirs(os.path.join(os.getcwd(), "..", dir_name))
    with open(os.path.join(os.getcwd(), "..", dir_name, file_name), "wb") as f:
        pickle.dump(model, f)

def load_model_sk(dir_name="text_mining_models", file_name="sklearn_model.pickle"):
    path = os.path.join(os.getcwd(), "..", dir_name, file_name)
    if os.path.isfile(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    else:
        model = create_model_sk()
        save_model_sk(model)
        return model

#model = load_model_sk()