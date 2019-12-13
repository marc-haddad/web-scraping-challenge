from flask import Flask, render_template, redirect
import pymongo
from flask_pymongo import PyMongo

import scrape_mars

# Configure app
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape_mars_app")

@app.route("/scrape")
def scrape_route():

    scrape_collection = mongo.db.scrape_collection
    scrape_data = scrape_mars.scrape()
    
    scrape_collection.update({}, scrape_data, upsert=True)

    return redirect("/", code=302)

@app.route("/")
def index():

    scrape_stuff = mongo.db.scrape_collection.find_one()

    return render_template("index.html", scrape_stuff=scrape_stuff)


if __name__=="__main__":
    app.run(debug=True)