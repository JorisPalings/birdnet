import sqlite3
from flask import g, Flask, jsonify

app = Flask(__name__)

DATABASE = 'detections.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/detections", methods=["GET"])
def get_detections():
    detections = query_db('SELECT * FROM DETECTION ORDER BY id DESC')
    response = jsonify(detections)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, 200

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
