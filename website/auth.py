from flask import Blueprint, render_template, request, redirect

auth = Blueprint('auth', __name__)  # allows routes to be called in other files


@auth.route('/login', methods = ['POST','GET'])
def login():
    
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
                
    return render_template('login.html')


@auth.route('/logout', methods = ['POST','GET'])
def logout():
    
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
                
    return render_template('home')


@auth.route('/sign-up', methods = ['POST','GET'])
def sign_up():
    
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
                
    return render_template('sign_up.html')
