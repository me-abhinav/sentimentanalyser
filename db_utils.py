import os
import sqlite3

db_name = 'training_data.sqlite'
db_table_name = 'training_data_table'
db_root = 'db'
db_path = os.path.join(db_root, db_name)


def create_new_db():
    if not os.path.exists(db_root):
        os.makedirs(db_root)

    if os.path.exists(db_path):
        os.remove(db_path)

    db = open_db()
    c = db.cursor()
    c.execute('CREATE TABLE ' + db_table_name + ' (text TEXT, sentiment INTEGER, date TEXT)')
    db.commit()
    db.close()


def open_db():
    db = sqlite3.connect(db_path)
    return db


def clear_db(db):
    c = db.cursor()
    c.execute('DROP TABLE ' + db_table_name)
    c.execute('CREATE TABLE ' + db_table_name + ' (text TEXT, sentiment INTEGER, date TEXT)')
    db.commit()


def insert_into_db(db, text, sentiment):
    c = db.cursor()
    c.execute('INSERT INTO ' + db_table_name + ' (text, sentiment, date) VALUES (?, ?, Datetime("now"))',
              (text, sentiment))
    db.commit()


def fetch_all_from_db(db):
    c = db.cursor()
    c.execute('SELECT * FROM ' + db_table_name)
    for row in c:
        yield row


if __name__ == '__main__':
    create_new_db()


