import pyrebase
import time

"""
This python file was used to debug pushing and retrieving user data
and is now being kept as a test utility/demo. It does nothing within our main
program.
"""


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
auth = firebase.auth()

email = 'python@python.com'
password = 'python'
user = auth.sign_in_with_email_and_password(email, password)

print('full user information: ')
print(str(user))


user_id = user['localId']
print('local id is : ' + user_id)
data = {
    "username": "default"
}
results = db.child("users").child(user_id).update(data)

username = db.child("users").child(user_id).child("username").get().val()
userhash = db.child("users").child(user_id).get().val()
print('userhash is: ' + str(userhash))
print('username is: ' + str(username))