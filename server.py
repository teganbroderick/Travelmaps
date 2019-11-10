from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
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
    if 'user_id' in session: #if session exists
        user = User.query.filter_by(user_id=session['user_id']).first()
        maps = Map.query.filter_by(user_id=session['user_id']).all()
        return render_template("profile.html", user=user, maps=maps)
    else:
        return render_template("homepage.html")

@app.route('/about')
def about():
    """about page"""

    return render_template("about.html")


@app.route('/login')
def login():
    """redirect to login.html"""

    return render_template("login.html")


@app.route('/login_process', methods=["POST"])
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
        #add user to session
        session['user_id'] = user.user_id
        flash("Logged in!")
        return render_template("profile.html", user=user, maps=user.maps)


@app.route('/signup_process', methods=["POST"])
def signup_process():
    """Check to see if user exists, if not, add user to user table"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    #check to see if email address is in the user table
    user_email = User.query.filter_by(email=email).first()

    if user_email == None: #if user email is not in the users table
        #add user to database
        user_info = User(fname=fname, lname=lname, email=email, password=password)
        db.session.add(user_info)
        db.session.commit()
        #get user object from database
        user = User.query.filter_by(email=email).first()       
        #add user to session
        session['user_id'] = user.user_id        
        flash("Logged in!")
        return render_template("profile.html", user=user, maps=user.maps)
    
    else: 
        flash("A user with that email address already exists.")
        return redirect("/login")


@app.route('/logout')
def logout():
    """delete user_id info from session and log user out"""
    
    del session["user_id"]
    flash("Logged out!")
    return redirect('/')


@app.route('/make_map')
def makemap():
    """redirect to new_map.html"""

    return render_template("newmap.html")


@app.route('/make_map_process')
def makemap_process():
    """Check to see if map exists, if not, add map to maps table"""

    map_name = request.args.get("map_name")
    map_description = request.args.get("map_description")

    #check to see if map_name and map_description are already in the maps table for logged in user
    map_to_verify = Map.query.filter_by(user_id=session['user_id'], 
                                        map_name=map_name, 
                                        map_description=map_description).first()
    
    if map_to_verify == None: #if new map is not in the maps table
        #Add new map to maps table in db
        map_info = Map(user_id=session['user_id'], 
                        map_name=map_name, 
                        map_description=map_description)
        db.session.add(map_info)
        db.session.commit()
        #get map object
        new_map = Map.query.filter_by(map_name=map_name, map_description=map_description).first()
        # redirect_route = "/map/" + str(new_map.map_id)
        return redirect(f'/map/{new_map.map_id}')
    else:
        flash("A map with that name and description already exists.") #make more specific to user, use name
        return redirect("/make_map")


@app.route('/map/<int:map_id>')
def render_map(map_id):
    """Render map.html for map_id passed into route"""

    user_map = Map.query.filter(Map.map_id == map_id).one()
    places_on_map = Place.query.filter(Place.map_id == map_id).all()
    #try and error for map ids that dont exist - handle error

    #return render_template("test_map_searchbox2.html", map=user_map)
    return render_template("map.html", map=user_map, places=places_on_map)


@app.route('/map/<int:map_id>/save', methods=["POST"]) 
def save_location(map_id):
    """Save marker to database places table, using current map_id"""
    
    user_map = Map.query.filter(Map.map_id == map_id).one()

    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    title = request.form.get('title')

    place_to_verify = Place.query.filter_by(map_id=map_id, 
                                            latitude=latitude, 
                                            longitude=longitude, 
                                            google_place_name=title).first()

    if place_to_verify == None: #if place isn't in database for that particular map
        #add place to places table in db
        new_place = Place(map_id=map_id, 
                            latitude=latitude, 
                            longitude=longitude, 
                            google_place_name=title)
        db.session.add(new_place)
        db.session.commit()
        
        places_on_map = Place.query.filter(Place.map_id == map_id).all()
        last_place_added = places_on_map[-1]
        print("HERE is the map!")
        print(user_map)
        print("HERE ARE PLACES ON MAP")
        print(places_on_map)
        print("HERE is last place added!")
        print(last_place_added)

        return render_template("map.html", map=user_map, places=places_on_map)
    else:
        flash("You already saved that location to your map")
        return render_template("map.html", map=user_map, places=places_on_map)

@app.route('/save_location.json')
def save_location_json():
    """Save marker to database places table from AJAX request using current map_id,
    return jsonified place"""

    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    title = request.args.get('title')
    map_id = request.args.get('map_id')

    #add place to places table in db
    new_place = Place(map_id=map_id, 
                        latitude=latitude, 
                        longitude=longitude, 
                        google_place_name=title)
    db.session.add(new_place)
    db.session.commit()
    print("Added place!")
    print(new_place)

    #get new place as an object
    new_place_object = Place.query.filter(Place.map_id == map_id, 
                                Place.latitude == latitude, 
                                Place.longitude == longitude).first()
    
    #make places list with nested dict
    place_object_attributes = [{}]
    temp_dict[0]['place_id'] = new_place_object.place_id
    temp_dict[0]['map_id'] = new_place_object.map_id
    temp_dict[0]['latitude'] = float(new_place_object.latitude)
    temp_dict[0]['longitude'] = float(new_place_object.longitude)
    temp_dict[0]['title'] = new_place_object.google_place_name

    return jsonify(place_object_attributes)


@app.route('/get_places/')
def get_places():
    """JSON information about places saved to map"""
    
    map_id = request.args.get("map_id")
    
    places_on_map = Place.query.filter(Place.map_id == map_id).all()
    places_list = []
    for place in places_on_map:
        temp_dict = {}
        temp_dict['place_id'] = place.place_id
        temp_dict['map_id'] = place.map_id
        temp_dict['latitude'] = float(place.latitude)
        temp_dict['longitude'] = float(place.longitude)
        temp_dict['title'] = place.google_place_name
        places_list.append(temp_dict)

    return jsonify(places_list)

@app.route('/get_last_place_added/')
def get_last_place_added():
    """JSON information about last place saved to map"""
    
    map_id = request.args.get("map_id")
    
    all_places_on_map = Place.query.filter(Place.map_id == map_id).all()
    if all_places_on_map != []:
        last_place_added = all_places_on_map[-1]

        print("HERE ARE PLACES ON MAP")
        print(all_places_on_map)
        print("HERE is last place added!")
        print(last_place_added)

        last_place_added_dict = {}
        last_place_added_dict['latitude'] = float(last_place_added.latitude)
        last_place_added_dict['longitude'] = float(last_place_added.longitude)
        print(last_place_added_dict)
        print("last_place_added_dict")
    else:
        last_place_added_dict = []

    return jsonify(last_place_added_dict)


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