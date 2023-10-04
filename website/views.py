from flask import Blueprint, render_template

# allows routes to be called in other files
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about-us')
def aboutus():
    return render_template("aboutus.html")