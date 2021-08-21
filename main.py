import os
from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)


def _get_history(house):
    cur = mongo.db.dollar.find({"house": house}, {
                                '_id': False, 'house': True, 'buy': True, 'sell': True, 'date': True})
    result = []
    for row in cur:
        result.append({
            "compra": row.get('buy'),
            "venta": row.get('sell'),
            "fecha": row.get('date')})
    return result


@app.route("/v1")
def home():
    cur_last = mongo.db.dollar.find().sort("date",-1).limit(4)
    last = []
    for row in cur_last:
        last.append({
                "tienda": row.get("house"),
                "compra": row.get("buy"),
                "venta": row.get("sell")})
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