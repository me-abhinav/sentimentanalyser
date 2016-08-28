import pandas as pd
import numpy as np
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.externals import joblib
from vectorizer import vect

df = pd.read_csv('data_combined.csv')
not_3 = df['rating'] != 3
df = df[not_3]

X = (df['title'] + ' # ' + df['comment']).values
X = vect.transform(X)
y = df['rating'].values
y = np.where(y < 3, 0, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7)
clf = joblib.load('../pkl_objects/clf.pkl')
classes = np.array([0, 1])

# clf.fit(X, y)
# joblib.dump(clf, '../pkl_objects/clf.pkl')

# clf.fit(X_train, y_train)
# for sample_X, sample_y in zip(X_test, y_test):
#     clf.partial_fit(sample_X, [sample_y], classes=classes)
# print(clf.score(X_test, y_test))
# scores = cross_val_score(clf, X, y, scoring='accuracy')
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

