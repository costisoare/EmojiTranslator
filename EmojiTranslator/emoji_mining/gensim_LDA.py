import gensim
import gensim.corpora as corpora
import pandas
import re
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def predict_topic(text, model):
    words = gensim.utils.simple_preprocess(str(text), deacc=True)

    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
    lemmatizer = WordNetLemmatizer()

    data_lemmatized = list()

    data_lemmatized.append([lemmatizer.lemmatize(w) for w in words if w not in stop_words])
    id2word = corpora.Dictionary(data_lemmatized)
    texts = data_lemmatized
    corpus = [id2word.doc2bow(text) for text in texts]

    unseen_doc = corpus[0]
    vector = sorted(model[unseen_doc], key=lambda x: x[1], reverse=True)
    return vector

def create_model(data="20newsgroups"):
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

    df = pandas.read_json('https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json')

    # Convert to list
    data = df.content.values.tolist()
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

    return gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=20)

def save_model(model, dir_name="text_mining_models", file_name="gensim_model"):
    if not os.path.exists(os.path.join(os.getcwd(), "..", dir_name)):
        os.makedirs(os.path.join(os.getcwd(), "..", dir_name))
    model.save(os.path.join(os.getcwd(), "..", dir_name, file_name))

def load_model(dir_name="text_mining_models", file_name="gensim_model"):
    path = os.path.join(os.getcwd(), "..", dir_name, file_name)
    if os.path.isfile(path):
        return gensim.models.ldamodel.LdaModel.load(path)
    else:
        model = create_model()
        save_model(model, file_name="gensimLDA")
        return model