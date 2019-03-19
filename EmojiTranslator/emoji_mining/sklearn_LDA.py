import os
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import LatentDirichletAllocation

class ModelVectorizer(object):
    def __init__(self, model, vectorizer):
        self.lda_model = model
        self.vectorizer = vectorizer

def predict_topic(text, model):
    tf = model.vectorizer.transform([text])
    topic_probability_scores = model.lda_model.transform(tf)
    return topic_probability_scores

def create_model(data="20newsgroups"):
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000,
                                    stop_words='english')
    dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
    documents = dataset.data
    tf = tf_vectorizer.fit_transform(documents)

    no_topics = 20
    lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    return ModelVectorizer(lda, tf_vectorizer)

def save_model(model, dir_name="text_mining_models", file_name="sklearn_model.joblib"):
    if not os.path.exists(os.path.join(os.getcwd(), "..", dir_name)):
        os.makedirs(os.path.join(os.getcwd(), "..", dir_name))
    dump(model, os.path.join(os.getcwd(), "..", dir_name, file_name))

def load_model(dir_name="text_mining_models", file_name="sklearn_model.joblib"):
    path = os.path.join(os.getcwd(), "..", dir_name, file_name)
    if os.path.isfile(path):
        return load(path)
    else:
        model = create_model("20newsgroups")
        save_model(model)
        return model