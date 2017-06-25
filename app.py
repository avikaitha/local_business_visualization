from flask import Flask
from flask import render_template
from flask import redirect,url_for,request
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
import get_keyword_analysis

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'yelp_dataset'
COLLECTION_NAME = 'yelp_business'





@app.route("/")
def index():
    if request.method == 'POST':
        # replace this with an insert into whatever database you're using
        result = request.args
        print request.args
        return redirect(url_for('dashboard', result_id=result.id))

    return render_template("search_index.html")


@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)
