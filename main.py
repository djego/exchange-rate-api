import json
import os
from flask import Flask, jsonify
from flask_pymongo import PyMongo

max_result = 8
app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)

houses_extra = {}
with open('./houses.json') as jsonfile:
    houses_extra = json.load(jsonfile)


def _get_history(house):
    cur = mongo.db.dollar.find({"house": house}, {
        '_id': False, 'house': True, 'buy': True,
        'sell': True, 'date': True}).sort('date', -1)
    result = []
    for row in cur:
        result.append({
            "compra": row.get('buy'),
            "venta": row.get('sell'),
            "fecha": row.get('date')})
    return result


@app.route("/v1/resume")
def home():
    cur_last = mongo.db.resume.find().sort(
        [("sell", 1)])
    last = []
    for row in cur_last:
        last.append({
            "tienda": row.get("house"),
            "compra": row.get("buy"),
            "venta": row.get("sell"),
            "fecha": row.get("date"),
            "url": houses_extra[row.get("house")]["url"],
            "image": houses_extra[row.get("house")]["image"]
        })
    return jsonify(last)


@app.route("/v1/tkambio")
def tkambio():
    history = _get_history("Tkambio")
    return jsonify(history)


@app.route("/v1/cambioseguro")
def cambioseguro():
    history = _get_history("Cambioseguro")
    return jsonify(history)


@app.route("/v1/rextie")
def rextie():
    history = _get_history("Rextie")
    return jsonify(history)


@app.route("/v1/kambista")
def kambista():
    history = _get_history("Kambista")
    return jsonify(history)
