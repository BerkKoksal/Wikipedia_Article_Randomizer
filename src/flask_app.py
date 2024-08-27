from flask import Flask,redirect,url_for,render_template,session,url_for
import wikipediaapi
import datetime
from datetime import *
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import random 
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
import re
import hashlib
from flask import request
app = Flask(__name__)


    #global vars

app.secret_key = 'essek'  # Replace with a secret key for session management

    #database connection details
# app.config["MYSQL_HOST"] = "BerkK.mysql.pythonanywhere-services.com"
# app.config["MYSQL_USER"] = "BerkK"
# app.config["MYSQL_PASSWORD"] = "osas1234"
# app.config["MYSQL_DB"] = "BerkK$userlogin"

    #initialize mysql
# mysql = MySQL(app)

class globalvars:
    '''global variable class going to be used for many functions'''
    shared_wikipedia_url = None
    last_update_time = None #when was site last updated?
    update_interval = 86400 #seconds = 1 day


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

def count(title):
   wiki_wiki = wikipediaapi.Wikipedia('WikipediaRandomGen/0.0 (erkanbobo33@gmail.com)', 'en')
   page_py = wiki_wiki.page(title)
   page_content = page_py.text

   soup = BeautifulSoup(page_content, 'html.parser')
   text_content = soup.get_text()
   tokens = word_tokenize(text_content)
   word_count = len(tokens)
   
   return word_count

def refrshsite(date_now):
    next_time = datetime(seconds = 10) 
    while(date_now < date_now + next_time):
        continue
    
    refresh()

def read_time_f(word_count):
    return word_count / 200

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


#login page
# @app.route("/login/", methods = ["POST"])
# def login():
#     #check if user submitted form is not empty
#     if request.method == "POST" and "username" in request.form and "password" in request.form:
#         #create vars username password
#         username = request.form["username"]
#         password = request.form["password"]

#         #get hashed password for encryption
#         hash = password + app.secret_key
#         hash = hashlib.sha1(hash.encode())
#         password = hash.hexdigest()

#         #check if account already exists
#         # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         # cursor.execute("SELECT * FROM accounts WHERE username = %s and password = %s",(username,password))
#         #fetch a record and return it
#         # account = cursor.fetchone()

#         #if account exists
#         if account():
#             #create session data using dictionaries 
#             session["loggedin"] = True
#             session["id"] = account["id"]
#             msg = f"Welcome {account}"
#             return(msg)

#             #Might want to put return statement to go back to home
#         else:
#             #account doesn't exist or wrong creditentials
#             msg = "Username/Password is incorrect."
#             return(msg)


@app.route("/Randomize/")
def regenerate():
   article_url, article_title = get_random_article() #get random article 
   word_count = count(article_title)
   read_time = read_time_f(word_count)
   return render_template("Randomize.html",  random_website = article_url, article_title = article_title, word_count = word_count, read_time = read_time)


# @app.route("/register/", methods = ["GET", "POST"])
# def register():
#     msg = ""
    
#     if request.method == "POST" and "username" in request.form and "password" in request.form and "email" in request.form:
#         username = request.form["username"]
#         password = request.form["password"]
#         email = request.form["email"]

#     elif request.form == "POST":
#     #data submitted but empty
#         msg = "Please enter your information."

#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT FROM accounts WHERE username = %s",(username,))
#     account = cursor.fetchone

#     #check if account exists 
#     if account:
#         msg = "Account already exists! Please try logging in."
    
#     #if doesn't exist check these conditions:
#     elif not re.match(r"[A-Za-z0-9]+", username):
#         msg = "Username can only contain letters and numbers!"
#     elif not re.match(r"[^@] + @[^@]+\.[^@]+", email):
#         msg = "Please enter a valid email."

#     elif not username or password or email:
#         msg = "Please fill out the form!"
    
#     else:
#         #hash the password
#         hash = password + app.secret_key
#         hash = hashlib.sha1(hash.encode())
#         password = hash.hexdigest()

#         #insert account details into new row
#     cursor.execute("INSTERT INTO accounts VALUES (Null, %s,%s,%s)",(username,password,email,))
#     mysql.connection.commit()
#     msg = f"Your account has been registered, welcome {account}!"
#     return render_template("home.html", msg = msg)

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/WikiBattle.html/")
def wikibattle():
    if session["loggedin"] == True:
        #user is logged in
        return render_template("home.html", username = session["username"])

    else:
        return redirect(url_for("login"))

    


@app.route("/Daily/")
def dailyrandom():
    home = globalvars
    headers = {
        "User-Agent": "WikipediaRandomGen/0.0 (https://github.com/BerkKoksal/Wikipedia_Article_Randomizer; erkanbobo33@gmail.com)"
    }

    # if 'current_hyperlink' not in session:
    #     # If there is no stored hyperlink in the session, get a new one
    #     session['current_hyperlink'] = get_random_hyperlink()
    
    current_time = datetime.now()
    if home.last_update_time is None or (current_time - home.last_update_time).seconds >= home.update_interval:
        home.last_update_time = current_time
        home.shared_wikipedia_url = get_random_hyperlink()
        home.last_update_time = current_time
    
    title = titleextractor(home.shared_wikipedia_url)
    word_count = count(title)
    read_time = read_time_f(word_count)
    return render_template("Template.html", article_title= title.replace("_"," "), todays_website = home.shared_wikipedia_url, word_count = word_count, read_time = read_time)

@app.route("/logout/")
def logout():
    #remove session data from dictionary effectively removing userdata
    session.pop("loggedin",None)
    session.pop("id", None)
    session.pop("username", None)

    #return to ghome
    return redirect(url_for("home"))
@app.route("/refresh")
def refresh():
    # Refresh the stored hyperlink in the session
    session['current_hyperlink'] = get_random_hyperlink()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug= True)



