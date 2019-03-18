import gensim
import gensim.corpora as corpora
import pandas
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def sent_to_words(sentences):
    words = list()
    for sentence in sentences:
        words.append(gensim.utils.simple_preprocess(str(sentence), deacc=True)) # deacc=True removes punctuations
    return words

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

data_words = list(sent_to_words(data))

lemmatizer = WordNetLemmatizer()
data_lemmatized = [[lemmatizer.lemmatize(w) for w in sent] for sent in data_words]

id2word = corpora.Dictionary(data_lemmatized)
texts = data_lemmatized
corpus = [id2word.doc2bow(text) for text in texts]

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=20)

other_texts = [
    ['computer', 'time', 'graph'],
    ['survey', 'response', 'eps'],
    ['human', 'system', 'computer']
]

id2word = corpora.Dictionary(other_texts)
other_corpus = [id2word.doc2bow(text) for text in other_texts]
unseen_doc = other_corpus[0]
vector = lda_model[unseen_doc]  # get topic probability distribution for a document
