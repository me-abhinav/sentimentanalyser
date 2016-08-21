from flask import g, jsonify, request
import os
from sklearn.externals import joblib
from vectorizer import vect
import numpy as np
import utils
import db_utils


__all__ = ['make_json_app']
app = utils.make_json_app(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = db_utils.open_db()
    return db


def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def api_root():
    result = {
        'message': 'Abhinav Chauhan is awesome :)'
    }
    return jsonify(result)


@app.route('/predict', methods=['POST'])
@utils.catch_exceptions(app.logger)
def predict():
    json = request.get_json(force=True)
    text = json["text"]
    X = vect.transform([text])
    prediction = label[clf.predict(X)[0]]
    probability = clf.predict_proba(X).max() * 100
    result = {
        "prediction": prediction,
        "probability": probability
    }
    return jsonify(result)


@app.route('/train', methods=['POST'])
@utils.catch_exceptions(app.logger)
def train():
    json = request.get_json(force=True)
    text = json["text"]
    sentiment = json["sentiment"]

    db_utils.insert_into_db(get_db(), text, inverse_label[sentiment])

    X = vect.transform([text])
    y = [inverse_label[sentiment]]
    clf.partial_fit(X, y, classes=classes)

    result = {
        'message': 'success'
    }
    return jsonify(result)


@app.route('/sync_to_disk', methods=['GET'])
def sync_to_disk():
    clf_from_disk = joblib.load(os.path.join('pkl_objects', 'clf.pkl'))
    db = db_utils.open_db()

    for row in db_utils.fetch_all_from_db(db):
        text = row[0]
        sentiment = row[1]
        X = vect.transform([text])
        y = [sentiment]
        clf_from_disk.partial_fit(X, y, classes=classes)

    joblib.dump(clf, os.path.join('pkl_objects', 'clf.pkl'))
    db_utils.clear_db(db)
    db.close()
    return utils.success_message()


if __name__ == '__main__':
    label = {0: 'negative', 1: 'positive', 2: 'neutral'}
    inverse_label = {'negative': 0, 'positive': 1, 'neutral': 2}
    classes = np.array([0, 1, 2])
    clf = joblib.load(os.path.join('pkl_objects', 'clf.pkl'))

    if app.debug is not True:
        import logging
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 10, backupCount=5)
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

    app.run()

