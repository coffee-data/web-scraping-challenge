from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# Import custom scraper
import scraper_mars

# Create an instance for Flask app.
app = Flask(__name__)

# Create connection variable
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

@app.route("/")
def index():
    scraped_data = mongo.db.scraped_data.find_one()
    return render_template("index.html", scraped_data=scraped_data)


@app.route("/scrape")
def scraper():
    scraped_data = mongo.db.scraped_data
    scraped_data_data = scraper_mars.scrape()
    scraped_data.update({}, scraped_data_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)