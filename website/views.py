from flask import Blueprint, render_template, request, redirect, session, url_for

import pyrebase
import time
import requests
import json

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
db = firebase.database() # reference to our database

storage = firebase.storage() # reference to our storage

auth = firebase.auth() # reference to our auth service

# allows routes to be called in other files
views = Blueprint('views', __name__)

@views.app_errorhandler(404)
def handle404(e):
    # Does something if and only if a page returns a 404 error
    # A 404 error occurs when user tries to go to a bad URL
    return render_template("404.html")

@views.app_errorhandler(403)
def handle403(e):
    # Does something if and only if a page returns a 403 error
    # A 403 error occurs when user tries to access a page without being authorized
    return render_template("403.html")

@views.route('/', methods = ['POST','GET'])
def home():
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery == "":
                # user entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
            
    """
    get the 6 most played games in our database
    ordered queries require indexed database sections, more info at
    https://stackoverflow.com/questions/34968413/error-index-not-defined-add-indexon
    """
    mostPlayedList = db.child("games").order_by_child("plays").limit_to_first(6).get().val()
    
    for game in mostPlayedList:
        # fetch the game image for every game we want to display
        gameImagePath = "games/" + game + "/" + game + ".png"
        # requires None as a token for pyrebase - known issue since 2017
        imageURL = storage.child(gameImagePath).get_url(None)
        mostPlayedList[game]["imageURL"] = imageURL

    # supply a backup image for games with no image
    backupImage = storage.child("games/defaultGameImage.png").get_url(None)
    
    return render_template("home.html", gameList = mostPlayedList, backupImage = backupImage)


@views.route('/about-us', methods = ['POST','GET'])
def aboutus():
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery == "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
    
    return render_template("aboutus.html")


@views.route('/search/<query>', methods = ['POST','GET'])
def search(query=""):
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery == "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)

    # Gets all text after /search/ and saves it in the string "query".
    
    gameDBSnapshot = db.child("games").get().val()
    searchedList = dict()
    
    for game in gameDBSnapshot:
        """
        For every game, if the search query is in that the title, add
        that game to the list of games to display to the user.
        """
        imageURLS = list()
        if query.lower() in game.lower():
            searchedList[game]=gameDBSnapshot[game]
            
            gameImagePath = "games/" + game + "/" + game + ".png"
            
            # requires None as a token for pyrebase - known issue since 2017
            imageURL = storage.child(gameImagePath).get_url(None)
            
            searchedList[game]["imageURL"] = imageURL
    
    # Supply a backup image for games with no image
    backupImage = storage.child("games/defaultGameImage.png").get_url(None)
    
    return render_template("searchResults.html", gameList = searchedList, backupImage = backupImage)

@views.route('/account', methods = ['POST','GET'])
def account():
    try:
        # only works when user is signed in 
        print(session['user'])
    except KeyError:
        return render_template("403.html")
    user_id = session['user']
    username = db.child("users").child(user_id).child("username").get().val()
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery == "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
            
    return render_template("Account.html", username=username)

@views.route('/games', methods = ['POST','GET'])
def games():
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery == "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
            
    return render_template("Games.html")

@views.route('/login', methods = ['POST','GET'])
def login():
    try:
        # only works when user is signed in 
        print(session['user'])
        # user is signed in, redirect them to account page
        return redirect('/account')
    except KeyError:
       # user is not signed in, let them access login page 
       pass

    message = ""
    # Check if this route was passed a message.
    try:
        session['message']
        print("Login was called with the passed message:")
        print(session['message'])
        message = session['message']
        del session['message']
    except KeyError:
        print("No message was passed to login.")

    if request.method == "POST":
        email = request.form["login_email"]
        print("email submitted: " + email)
        password = request.form["login_password"]
        print("password submitted: " + password)
        try:
            print("Attempting to login...")
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = user['localId']
            session['user'] = user_id
            username = db.child("users").child(user_id).child("username").get().val()
            if not username:
            # username does not exist, create a starting username
                data = {
                    "username": "default"
                }
                results = db.child("users").child(user_id).update(data)
            return redirect('/account')
        except Exception as e:
            print("An error has occured during login.")
            print("------------------Full http error------------------")
            print(e)

            e = str(e)

            print("-------------Error as displayed to user-------------")
            # Get the error part of the returned http error response
            start = e.find('\"message\"')
            end = e.find('\"errors\"')
            message = e[start+12:end-7]
            message = message.strip() # Removes newline character at the end

            """
            Replace returned message with a more user-friendly error message.
            There is only 1 known error passed back by firebase's login method.
            Please update this if more error messages are found.
            """
            
            if message == "INVALID_LOGIN_CREDENTIALS":
                message = "Incorrect email or password. Please login again."

            print(message)

    return render_template('login.html', message=message)


@views.route('/logout', methods = ['POST','GET'])
def logout():
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery == "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
            
    # attempt to delete session information, redirect logged out user to homepage
    try:
        del session['user']
        auth.signOut()
    except:
    # user accessed logout function without being signed in, do nothing, redirect
        pass
    return redirect('/')

@views.route('/sign-up', methods = ['POST','GET'])
def sign_up():
    try:
        # only works when user is signed in 
        print(session['user'])
        # user is signed in, redirect them to account page
        return redirect('/account')
    except KeyError:
       # user is not signed in, let them access sign_up page 
       pass

    print("request method = " + request.method)
    
    message = ""
    # Check if this route was passed a message.
    try:
        session['message']
        print("Login was called with the passed message:")
        print(session['message'])
        message = session['message']
        del session['message']
    except KeyError:
        print("No message was passed to sign-up.")

    if request.method == "POST":

        email = request.form['signup_email']
        print("email =  " + email)
        password = request.form['signup_password']
        print("password = " + password)
        try:
            print("Trying to sign up...")
            user = auth.create_user_with_email_and_password(email, password)
            message = "Signed up successfully. Please login."
            session['message'] = message
            return redirect(url_for('views.login'))
        except Exception as e:
            # Convert e from HTTPError to json to dict
            print("An error has occured during signup.")
            print("------------------Full http error------------------")
            print(e)

            e = str(e)

            print("-------------Error as displayed to user-------------")
            # Get the message part of the returned http error response
            start = e.find('\"message\"')
            end = e.find('\"errors\"')
            message = e[start+12:end-7]
            message = message.strip() # Removes newline character at the end

            # Replace returned message with a more user-friendly error message
            if message == "INVALID_EMAIL":
                message = "Please enter a valid email."
            elif message == "WEAK_PASSWORD : Password should be at least 6 characters":
                message = "Your password must contain at least 6 characters."
            elif message == "EMAIL_EXISTS":
                message = "An account with your email already exists."
                message += " Please use a different email or sign in instead."
            print(message)
            print("----------------------------------------------------")
                
    return render_template('SignUp.html', message=message)
  
@views.route('/profile/picture', methods = ['POST','GET'])
def picture():
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery is "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
            
    return render_template("account_profile.html")

@views.route('/account/inbox', methods = ['POST','GET'])
def inbox():
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery is "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
            
    return render_template("account_inbox.html")

@views.route('/account/favgames', methods = ['POST','GET'])
def favgames():
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery is "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
            
    return render_template("account_favgames.html")

@views.route('/account/messages', methods = ['POST','GET'])
def messages():
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery is "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
            
    return render_template("account_messages.html")

@views.route('/account/favgames', methods = ['POST','GET'])

@views.route('/account/changepas', methods = ['POST','GET'])
def changepassword():
    
    if request.method == "POST":
        if request.form.get("searchQuery"):
        # Submitted form is a search form
            searchQuery = request.form.get("searchQuery")
            
            if searchQuery is "":
                # User entered a blank form, return them to current page
                return redirect(request.path)
            else:
                redirectURL = "/search/" + searchQuery
                return redirect(redirectURL)
            
    return render_template("change_password.html")
