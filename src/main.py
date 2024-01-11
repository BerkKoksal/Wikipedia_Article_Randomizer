from flask import Flask,redirect,url_for,render_template,session
import wikipediaapi
import datetime
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import random 
app = Flask(__name__)


app.secret_key = 'your_secret_key'  # Replace with a secret key for session management

def get_random_hyperlink():
    archive_url = 'https://endwalker.com/archive.html'
    response = requests.get(archive_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        hyperlinks = [a['href'] for a in soup.find_all('a', href=True)]
        return random.choice(hyperlinks)
    else:
        return None

def titleextractor(url:str):
    title = url.replace("https://en.wikipedia.org/wiki/","")
    return title

@app.route("/")
def home():
    headers = {
        "User-Agent": "WikipediaRandomGen/0.0 (https://github.com/BerkKoksal/Wikipedia_Article_Randomizer; erkanbobo33@gmail.com)"
    }
    title = "default title"

    if 'current_hyperlink' not in session:
        # If there is no stored hyperlink in the session, get a new one
        session['current_hyperlink'] = get_random_hyperlink()
       
    
    title = titleextractor(str(session['current_hyperlink']))
    word_count = count(title)
    read_time = word_count / 200
    return render_template("Template.html", article_title= title.replace("_"," "), todays_website = session['current_hyperlink'], word_count = word_count, read_time = read_time)

@app.route("/refresh")
def refresh():
    # Refresh the stored hyperlink in the session
    session['current_hyperlink'] = get_random_hyperlink()
    return redirect(url_for('home'))
   
    

def count(title):
   wiki_wiki = wikipediaapi.Wikipedia('WikipediaRandomGen/0.0 (erkanbobo33@gmail.com)', 'en')
   page_py = wiki_wiki.page(title)
   page_content = page_py.text

   soup = BeautifulSoup(page_content, 'html.parser')
   text_content = soup.get_text()
   tokens = word_tokenize(text_content)
   word_count = len(tokens)
   
   return word_count

# def summary():
#    article_url , article_title = get_random_article()
   
#    wiki_wiki = wikipediaapi.Wikipedia(
#     user_agent='WikipediaRandomGen/0.0 (erkanbobo33@gmail.com)',
#         language='en',
#         extract_format=wikipediaapi.ExtractFormat.WIKI
# )
#    p_wiki = wiki_wiki.page("Test 1").text
#    return(p_wiki)





def get_random_article():
   '''Code to generate a random wikipedia article. Also includes User_Agent'''
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
   return(article_url, article_title)



@app.route("/Randomize.html/")
def regenerate():
   article_url, article_title = get_random_article() #get random article 
   word_count = count(article_title)
   read_time = word_count / 200
   return render_template("Randomize.html",  random_website = article_url, article_title = article_title, word_count = word_count, read_time = read_time)


if __name__ == "__main__":
    app.run()

