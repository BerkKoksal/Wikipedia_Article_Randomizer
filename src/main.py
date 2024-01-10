from flask import Flask,redirect,url_for,render_template
import wikipediaapi
import datetime
import requests

app = Flask(__name__)


# def decorator():
#     def wrapper(func):
#         home()
#         print("essek")

@app.route("/")
def home():
   
   return render_template("Template.html")

def word_count():
   

@app.route("/Randomize.html/")
def random():
   
   '''Code to generate a random wikipedia article. Also includes User_Agent'''
   wiki_topics = [
      "Mathematics",
      "Biology",
      "Physics",
      "Music",
      "Geography",
      "History",
      "Technology"
   ]
   
   day_of_the_week = datetime.datetime.today().weekday() #monday is 0, sunday is 6
    
   todays_topic = wiki_topics[day_of_the_week]
   headers = {
      "User_Agent" : "WikipediaRandomGen/0.0 (https://github.com/BerkKoksal/Wikipedia_Article_Randomizer; erkanbobo33@gmail.com)"
      }

   

   # wiki_wiki = wikipediaapi.Wikipedia("en")
   # selected_page = wiki_wiki.page(f"Portal:{todays_topic}")
   
   search_url = f'https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json&utf8='
   
   response = requests.get(search_url, headers=headers)
   data = response.json()
   article_title = data['query']['random'][0]['title']
   article_url = f'https://en.wikipedia.org/wiki/{article_title}'
   
   return render_template("Randomize.html",  random_website = article_url, article_title = article_title )


if __name__ == "__main__":
    app.run()

