import pyrebase

#Initialize Firebase and database
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
games = db.child("games").get().val()

def delete_game_by_name(game_name, games):
    # Query the database to find the game entry by name
    games = db.child("games").get().val()
    
    if games:
        for gameName, gameData in games.items():
            if gameName.lower() == game_name.lower():
                # Delete the game entry with the specified key
                db.child("games").child(gameName).remove()
                print(f"Deleted game '{game_name}' with key '{gameName}'")
                return
                
    # If the game with the specified name is not found
    print(f"Game '{game_name}' not found in the database")

# Prompt the user for the name of the game to delete
game_name_to_delete = input("Enter the name of the game to delete: ")
delete_game_by_name(game_name_to_delete, games)
