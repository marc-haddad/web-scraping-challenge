from flask import Flask, render_template
import pymongo

from scrape_mars import scrape 

# Configure app
#app = Flask(__name__)

# Configure MongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.scrape_db
# Call drop to avoid dups
db.scrape_db.drop()

results = scrape()
db.scrape_db.insert_many(results)

print(list(db.scrape_db.find()))