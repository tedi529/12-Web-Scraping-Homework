from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    
    mars_news = scrape_mars.scrape_news()
    mars_data.update({}, mars_news, upsert = True)
    
    mars_feat_image = scrape_mars.scrape_feat_image()
    mars_data.update({}, mars_feat_image, upsert = True)
    
    mars_weather = scrape_mars.scrape_weather()
    mars_data.update({}, mars_weather, upsert = True)
    
    mars_facts = scrape_mars.scrape_facts()
    mars_data.update({}, mars_facts, upsert = True)
    
    mars_hemispheres = scrape_mars.scrape_hemispheres()
    mars_data.update({}, mars_hemispheres, upsert = True)
    return redirect ("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
