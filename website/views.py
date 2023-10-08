from flask import Blueprint, render_template, request, redirect

import pyrebase
import time

# Firebase configuration 
firebase_config = {
    "apiKey": "AIzaSyBPqJ-k5eE3VvcwohxAPUjk0FtI9CmuQQk",
    "authDomain": "venom-36428.firebaseapp.com",
    "databaseURL": "https://venom-36428-default-rtdb.firebaseio.com",
    "projectId": "venom-36428",
    "storageBucket": "venom-36428.appspot.com",
    "messagingSenderId": "918438359333",
    "appId": "1:918438359333:web:3c95ae1e6ea1cb872eaacc",
    "measurementId": "G-6ML5XV7KN3"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# allows routes to be called in other files
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about-us')
def aboutus():
    return render_template("aboutus.html")

@views.route('/search/<query>', methods = ['POST','GET'])
def search(query):
    
    gamesSnapshot = db.child("games").get().val()
    searchedList = gamesSnapshot
    # gameNames=list(gamesSnapshot.keys())
    
    
    return render_template("searchResults.html", gameList = searchedList)