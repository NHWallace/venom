import pyrebase

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

#add data
#please use a valid url for each of these, we will be loading these images on the homepage later
game1data = {
"name": "tictactoe",
"iconurl": "https://t3.ftcdn.net/jpg/06/15/41/72/360_F_615417282_RM74va9wUJcqi8vt8vi8gVTxaQAutqr4.jpg",
"categories": "strategy",
"rating": "5",
"uploaderID":"randName"
}

db.child("games").push(game1data)
