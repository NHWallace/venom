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

gamesdb = db.child("games")

#add data
#please use a valid url for each of these, we will be loading these images on the homepage later

def update_game(data,databaseRef):

    gameName = list(data)[0]
    innerData = data[gameName]
    snapshot = databaseRef.get().val()
    firstUpload = None
    
    if snapshot is None or gameName not in snapshot :
        # uploading this game for the first time
        firstUpload = True
    else:
        # this game already exists in the database
        firstUpload = False
        
    # always update database with provided data
    databaseRef.child("games").child(gameName).update(innerData)
    
    # only initialize metadata for new games
    
    if firstUpload is True:
        
        currentTime = int(time.time()) # Unix timestamp

        extraData = {
            "uploadTime": currentTime,
            "rating": 0,
            "plays": 0,
            "favorites": 0
            }
        
        databaseRef.child("games").child(gameName).update(extraData)

"""
Our game data should be formatted as follow:
game1data = {
    "tictactoe": {
        "categories": "strategy",
        "uploaderID": "martin",
        "hasCSS": False,
        "hasJS": False
        }
}
"""

# Create 40 fake games to add to our list
gameData = list()
for x in range(40):
    gameName = "Game " + str(x+1)
    uploaderID = "user" + str(x+1)
    categories = ""
    
    if (((x+1) % 3) == 0):
        categories = "strategy"
    elif (((x+1) % 3) == 1):
        categories = "action"
    else:
        categories = "puzzle"
    
    gameData.append({
        gameName: {
            "categories": categories,
            "uploaderID": uploaderID,
            "hasCSS": False,
            "hasJS": False            
        }
    })
    
for game in gameData:
    update_game(game,gamesdb)
