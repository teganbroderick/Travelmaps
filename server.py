from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Map, Place, connect_to_db, db

import uuid

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Index page"""
    if 'user_id' in session: #if session exists
        user = User.query.filter_by(user_id=session['user_id']).first()
        maps = Map.query.filter_by(user_id=session['user_id']).all()
        return render_template("profile.html", user=user, maps=maps)
    else:
        return render_template("index.html")

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
    
    if map_to_verify == None: #if new map is not in the maps table, add new map to maps table in db
        url_hash = uuid.uuid4() #generate random uuid (universal unique identifier) for map
        map_hex = url_hash.hex
        map_info = Map(user_id=session['user_id'], 
                        map_name=map_name, 
                        map_description=map_description, 
                        map_url_hash=map_hex)
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
    """Render map.html for a map_id passed into the route"""

    user_map = Map.query.filter(Map.map_id == map_id).one()
    places_on_map = Place.query.filter(Place.map_id == map_id).all()
    #To do: handle error if user types a wrong number into the address bar
    
    user_id_for_map = user_map.user_id
    
    #If someone tries to access a map that isn't theirs, redirect to index page/profile
    if session["user_id"] != user_id_for_map:
        flash("You don't have permission to view that page!")
        return redirect("/")
    else:
        return render_template("map.html", map=user_map, places=places_on_map)


@app.route('/map/<int:map_id>/save', methods=["POST"]) 
def save_location(map_id):
    """Save marker to database places table, using current map_id"""

    title = request.form.get('title')
    address = request.form.get('address')
    website = request.form.get('website')
    place_types = request.form.get('types')
    google_places_id = request.form.get('google_places_id')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    user_notes = request.form.get('user_notes')

    user_map = Map.query.filter(Map.map_id == map_id).one()
    
    place_to_verify = Place.query.filter_by(map_id=map_id, 
                                            latitude=latitude, 
                                            longitude=longitude, 
                                            google_place_name=title, 
                                            place_active=True).first()

    if place_to_verify == None: #if place isn't in database for that particular map
        #add place to places table in db
        new_place = Place(map_id=map_id, 
                            google_place_name=title,
                            address=address,
                            website=website,
                            place_types=place_types,
                            google_places_id=google_places_id,
                            latitude=latitude, 
                            longitude=longitude, 
                            user_notes=user_notes)
        db.session.add(new_place)
        db.session.commit()
        places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()
        return render_template("map.html", map=user_map, places=places_on_map)  

    else:
        flash("You already saved that location to your map")
        places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()
        return render_template("map.html", map=user_map, places=places_on_map)


@app.route('/map/<int:map_id>/delete', methods=["POST"]) 
def delete_location(map_id):
    """Delete marker from database places table, using current map_id"""

    place_to_delete_id = request.form.get('google_places_id')

    place_to_delete = Place.query.filter(Place.google_places_id == place_to_delete_id, Place.map_id == map_id).first()
    #change place_active to false for place_to_delete. Place will no longer be rendered on the map.
    place_to_delete.place_active = False
    db.session.commit() 
    #get map and active places on map
    user_map = Map.query.filter(Map.map_id == map_id).one()
    places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()

    return render_template("map.html", map=user_map, places=places_on_map)


@app.route('/share_map<map_url_hash>')
def share_map():
    """create shareable version of current map usng crypotgraphic hash at end of address"""
    user_map = Map.query.filter(Map.map_url_hash == map_url_hash).one()
    places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()

    return render_template("share_map.html", map=user_map, places=places_on_map)


@app.route('/get_places/')
def get_places():
    """JSON information about places saved to map"""
    
    map_id = request.args.get("map_id")
    
    places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()
    places_list = []
    for place in places_on_map:
        temp_dict = {}
        temp_dict['google_places_id'] = place.google_places_id
        temp_dict['map_id'] = place.map_id
        temp_dict['latitude'] = float(place.latitude)
        temp_dict['longitude'] = float(place.longitude)
        temp_dict['title'] = place.google_place_name
        temp_dict['address'] = place.address
        temp_dict['website'] = place.website
        temp_dict['place_types'] = place.place_types
        temp_dict['user_notes']=  place.user_notes
        places_list.append(temp_dict)

    return jsonify(places_list)


@app.route('/get_last_place_added/')
def get_last_place_added():
    """JSON information about last place saved to map"""
    
    map_id = request.args.get("map_id")
    #get all active places on the map
    all_places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()
    #get last place added
    if all_places_on_map != []: #if there are places saved to the map
        last_place_added = all_places_on_map[-1]
        last_place_added_dict = {}
        last_place_added_dict['latitude'] = float(last_place_added.latitude)
        last_place_added_dict['longitude'] = float(last_place_added.longitude)
    else:
        last_place_added_dict = {} #set center to SF
        last_place_added_dict['latitude'] = float(37.7749295) 
        last_place_added_dict['longitude'] = float(-122.41941550000001)

    return jsonify(last_place_added_dict)


# @app.route('/save_location.json')
# def save_location_json():
#     """Save marker to database places table from AJAX request using current map_id,
#     return jsonified place"""
#     print("Made it to the save_location_json function")
#     map_id = request.args.get('map_id')
#     title = request.form.get('title')
#     address = request.form.get('address')
#     website = request.form.get('website')
#     place_types = request.form.get('types')
#     google_places_id = request.form.get('google_places_id')
#     latitude = request.form.get('latitude')
#     longitude = request.form.get('longitude')
#     user_notes = request.form.get('user_notes')

#     #add place to places table in db
#     new_place = Place(map_id=map_id, 
#                             google_place_name=title,
#                             address=address,
#                             website=website,
#                             place_types=place_types,
#                             google_places_id=google_places_id,
#                             latitude=latitude, 
#                             longitude=longitude, 
#                             user_notes=user_notes)
#     db.session.add(new_place)
#     db.session.commit()
#     print("Added place!")
#     print(new_place)

#     #get new place as an object
#     new_place_object = Place.query.filter(Place.map_id == map_id, 
#                                 Place.latitude == latitude, 
#                                 Place.longitude == longitude).first()
    
#     #make places list with nested dict
#     place_object_attributes = []
#     temp_dict = {}
#     temp_dict['google_places_id'] = place.google_places_id
#     temp_dict['map_id'] = place.map_id
#     temp_dict['latitude'] = float(place.latitude)
#     temp_dict['longitude'] = float(place.longitude)
#     temp_dict['title'] = place.google_place_name
#     temp_dict['address'] = place.address
#     temp_dict['website'] = place.website
#     temp_dict['place_types'] = place.place_types
#     temp_dict['user_notes']=  place.user_notes
#     place_object_attributes.append(temp_dict)

#     return jsonify(place_object_attributes)


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