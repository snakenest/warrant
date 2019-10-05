__author__ = 'Administrator'

# coding : utf-8

import pymongo
from flask import Flask
from flask import render_template
from settings import MONGO_URI, MONGO_DATABASE
import datetime
import pdb

app = Flask(__name__)
@app.route("/")
def hello():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    # pdb.set_trace()
    jokes = db["dict"].find( {"expiration_date":{ "$gt" : datetime.datetime(2020,3,1,0,0) } } ).sort("earnings_24", pymongo.DESCENDING)
    client.close()
    return render_template("warrant.html", p_jokes = jokes)

if __name__ == "__main__":
    app.run(debug = True, threaded = True)
