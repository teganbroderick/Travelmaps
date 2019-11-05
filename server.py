from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Map, Place, UserPlace, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")


@app.route("/login")
def login():
    """redirect to login.html"""

    return render_template("login.html")


@app.route("/login_process", methods=["POST"])
def login_process():
    """Verify email and password credentials, log user in if they are correct"""

    email = request.form.get("email")
    password = request.form.get("password")

    #check to see if email address and password match a user in the users table
    user = User.query.filter_by(email=email, password=password).first()

    if user == None:
        flash("Wrong email or password. Try again!")
        return redirect('/login')
    else:
        #get user object
        user = User.query.filter_by(email=email, password=password).first()

        #add user to session
        session['user_id'] = user.user_id
        flash("Logged in!")
        return render_template("profile.html", fname=user.fname, lname=user.lname)


@app.route("/signup_process", methods=["POST"])
def signup_process():
    """Check to see if user exists, if not, add them to user table"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    #check to see if email address is in the user table
    user_email = User.query.filter_by(email=email).first()

    if user_email == None: #if user email is not in the user table
        #add user to database
        user_info = User(fname=fname, lname=lname, email=email, password=password)
        db.session.add(user_info)
        db.session.commit()

        #get user object from database
        user = User.query.filter_by(email=email, password=password).first()
        
        #add user to session
        session['user_id'] = user.user_id 
        print("HEREEEEEE")
        print("SESSION INFO:", session['user_id'])
        print("")
        print("")
        print("")
        flash("Logged in!")

        return render_template("profile.html", fname=user.fname, lname=user.lname)
    
    else: 
        flash("User with that email address already exists.")
        return redirect("/login")

@app.route("/logout")
def logout():
    """delete user_id info from session and log user out"""
    
    del session["user_id"]
    flash("Logged out!")
    
    return redirect('/')

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')