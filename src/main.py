from flask import Flask,redirect,url_for,render_template
import wikipediaapi
import datetime

app = Flask(__name__)


# def decorator():
#     def wrapper(func):
#         home()
#         print("essek")

@app.route("/")
def home():
   
   wiki_topics = [
      "Math",
      "Biology",
      "Physics",
      "Music",
      "Geography",
      "History",
      "Technology"
   ]
   
   day_of_the_week = datetime.datetime.today().weekday() #monday is 0, sunday is 6
    
   todays_topic = wiki_topics[day_of_the_week]

   wiki_wiki = wikipediaapi.Wikipedia("en")
   selected_page = wiki_wiki.page(f"Portal:{todays_topic}")
   
   print(selected_page.fullurl)
   return render_template("Template.html", todays_website = selected_page.fullurl)
    


if __name__ == "__main__":
    app.run()

