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
    mars_listings = mongo.db.mars_listings.find_one()
    return render_template("index.html", mars_listings=mars_listings)


@app.route("/scrape")
def scraper():
    mars_listings = mongo.db.mars_listings
    listings_data = scraper_mars.scrape()
    mars_listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)