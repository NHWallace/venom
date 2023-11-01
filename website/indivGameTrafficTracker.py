import pyrebase

# Initialize Firebase and database
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

def record_game_play(game_name, player_id, favorited, games):
    games_path = db
    game_play_path = db
    unique_players_path = db
    favorites_path = db
    # Retrieve the games data
    games = db.child("games").get().val()
    # Check if the specified game exists in the database
    if games:
        for gameName, gameData in games.items():
            if game_name not in games:
                print(f"Game '{game_name}' does not exist in the database.")
                return

            # Update the play count
            play_count = games[game_name].get("play_count", 0)
            db.child("games").child(game_name).child("play_count").set(play_count + 1)

            # Check if the player is unique
            unique_players = games[game_name].get("unique_players", [])
            if player_id not in unique_players:
                unique_players.append(player_id)
                db.child("games").child(game_name).child("unique_players").set(unique_players)

            # Update the favorite count
            favorite_count = games[game_name].get("favorite_count", 0)
            if favorited:
                db.child("games").child(game_name).child("favorite_count").set(favorite_count + 1)

# Retrieve the games data
games = db.child("games").get().val()

# Automatically retrieve the game name and player ID (replace with your actual logic)
# For example, you might get these values from user input or session data
game_name = "Game 1"
player_id = "user1"
favorited = True  # Set to True if the game is favorited, otherwise set to False

# Record the game play
record_game_play(game_name, player_id, favorited, games)

