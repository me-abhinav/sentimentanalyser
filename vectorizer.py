from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.externals import joblib
import re
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
pkl_objects = os.path.join(PROJECT_ROOT, 'pkl_objects')
stop = joblib.load(os.path.join(pkl_objects, 'stopwords.pkl'))


def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',
                           text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) \
                   + ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized


vect = HashingVectorizer(decode_error='ignore',
                         n_features=2**21,
                         preprocessor=None,
                         tokenizer=tokenizer)

