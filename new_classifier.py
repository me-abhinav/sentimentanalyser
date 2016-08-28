import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib
import os
import numpy as np

stop = stopwords.words('english')


def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized


vect = HashingVectorizer(decode_error='ignore',
                         n_features=2**21,
                         preprocessor=None,
                         tokenizer=tokenizer)

clf = SGDClassifier(loss='log', random_state=1, n_iter=1)

example0 = ["This app is bad"]
example1 = ["This app is good"]

classes = np.array([0, 1])
# 0 is negative
# 1 is positive

clf.partial_fit(vect.transform(example0), [0], classes=classes)
clf.partial_fit(vect.transform(example1), [1], classes=classes)

dest = 'pkl_objects'
if not os.path.exists(dest):
    os.makedirs(dest)


joblib.dump(clf, os.path.join(dest, 'clf.pkl'))
joblib.dump(stop, os.path.join(dest, 'stopwords.pkl'))
