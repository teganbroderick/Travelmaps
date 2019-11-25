from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Map, Place, connect_to_db, db
import helpers

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Verify whether session exists, render index page"""
    if 'user_id' in session: #if session exists
        user = User.query.filter_by(user_id=session['user_id']).first()
        maps = Map.query.filter_by(user_id=session['user_id']).all()
        return render_template("profile.html", user=user, maps=maps)
    else:
        return render_template("index.html")

@app.route('/about')
def about():
    """Render about page"""

    return render_template("about.html")


@app.route('/login')
def login():
    """Redirect to login.html"""

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

    user = User.query.filter_by(email=email).first() #get user using entered email address

    if user == None: #if user is not in the users table
        helpers.add_user_to_database(fname, lname, email, password)
        user = helpers.log_in(email)
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

    return render_template("make_map.html")


@app.route('/make_map_process')
def makemap_process():
    """Check to see if map exists, if not, add map to maps table"""

    map_name = request.args.get("map_name")
    map_description = request.args.get("map_description")

    #check to see if map_name and map_description are already in the maps table for logged in user
    map_to_verify = Map.query.filter_by(user_id=session['user_id'], 
                                        map_name=map_name, 
                                        map_description=map_description).first()
    
    if map_to_verify == None: #if new map is not in maps table, add to db
        helpers.add_map_to_database(session['user_id'], map_name, map_description)
        new_map = Map.query.filter_by(user_id = session['user_id'], map_name=map_name, map_description=map_description).first() #get map object
        return redirect(f'/map/{new_map.map_id}')
    else:
        flash("A map with that name and description already exists.") #to do: make more specific to user, use name
        return redirect("/make_map")


@app.route('/map/<int:map_id>')
def render_map(map_id):
    """Render map.html for a map_id passed into the route"""

    user_map = Map.query.filter(Map.map_id == map_id).one()
    places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()
    #To do: handle error if user types a wrong number into the address bar
    user_id_for_map = user_map.user_id
    
    if session["user_id"] != user_id_for_map: #If user doesn't own the map
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

    if place_to_verify == None: #if place isn't in db for that particular map, add place to db
        helpers.add_place_to_database(map_id, title, address, website, place_types, google_places_id, latitude, longitude, user_notes)
        places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all() #get active places on map
        return render_template("map.html", map=user_map, places=places_on_map)  

    else:
        flash("You already saved that location to your map")
        places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()
        return render_template("map.html", map=user_map, places=places_on_map)


@app.route('/map/<int:map_id>/delete', methods=["POST"]) 
def delete_location(map_id):
    """Delete marker from database places table, using current map_id"""

    place_to_delete_id = request.form.get("google_places_id")

    place_to_delete = Place.query.filter(Place.google_places_id == place_to_delete_id, Place.map_id == map_id).first()
    #change place_active to false for place_to_delete. Place will no longer be rendered on the map.
    place_to_delete.place_active = False
    db.session.commit() 
    #get map and active places on map
    user_map = Map.query.filter(Map.map_id == map_id).one()
    places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()

    return render_template("map.html", map=user_map, places=places_on_map)


@app.route('/share_map/<map_url_hash>')
def share_map(map_url_hash):
    """Create shareable version of current map usng crypotgraphic hash at end of address"""
    user_map = Map.query.filter(Map.map_url_hash == map_url_hash).one()
    map_id = user_map.map_id
    places_on_map = Place.query.filter(Place.map_id == map_id, Place.place_active == True).all()
    map_url = "http://0.0.0.0:5000/share_map/" + user_map.map_url_hash

    return render_template("share_map.html", map=user_map, places=places_on_map, map_url=map_url)


@app.route('/dashboard')
def dashboard():
    """Get user statistics, render internal dashboard html page"""

    total_users = len(User.query.filter().all())
    print("total users", total_users)
    total_maps = len(db.session.query(Map.map_id).all())
    print("total maps", total_maps)
    total_places_mapped = len(Place.query.filter().all())
    print("total places mapped", total_places_mapped)
    avg_places_mapped = round(total_places_mapped / total_maps, 2)
    avg_maps_per_user = round(total_maps / total_users, 2)

    return render_template("dashboard.html", 
                            total_users=total_users, 
                            total_maps=total_maps, 
                            total_places_mapped=total_places_mapped,
                            avg_places_mapped=avg_places_mapped,
                            avg_maps_per_user=avg_maps_per_user)


@app.route('/place_type_statistics.json')
def get_place_type_statistics():
    """Get JSON object with top 5 place types saved to all maps"""

    all_places = db.session.query(Place.place_types).all() #get all places, returns list of tuples
    
    place_type_dictionary = {} #make dictionary with key: place type, value: number of times place type has been added to a map
    for place in all_places:
        #split string in tuple into individual place types
        types = place[0].split(",") 
        #get first place type tag from each place, make dictionary with place types and count
        if place_type_dictionary.get(types[0]) == None:
            place_type_dictionary[types[0]] = 1
        else:
            place_type_dictionary[types[0]] += 1
    
    data = sorted(place_type_dictionary.values(), reverse=True) #sort dict on values
    labels = sorted(place_type_dictionary, key=place_type_dictionary.__getitem__, reverse=True) #get key associated with sorted values

    data_dict = {
                "labels": labels[0:5],
                "datasets": [
                    {
                        "data": data[0:5],
                        "backgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56",
                            "#74D3AE",
                            "#f29559",
                        ],
                        "hoverBackgroundColor": [
                        ]
                    }]
            }

    return jsonify(data_dict)


@app.route('/place_statistics.json')
def get_place_statistics():
    """Get JSON object with top 10 places saved to all maps"""
    
    all_places = db.session.query(Place.google_place_name, Place.google_places_id).all() #get all places, returns list of tuples

    place_dictionary = {} #make dictionary with key: (place name,google_places_id), value: number of times place has been added to a map
    for place in all_places:
        if place_dictionary.get(place) == None:
            place_dictionary[place] = 1
        else:
            place_dictionary[place] += 1 
    
    data = sorted(place_dictionary.values(), reverse=True) #sort dict on values
    labels = sorted(place_dictionary, key=place_dictionary.__getitem__, reverse=True) #get key associated with sorted values
    
    #Get place names out of place tuples
    name_labels = []
    for i in range(0,10):
        name_only = labels[i][0]
        name_labels.append(name_only)
    
    data_dict = {
            "labels": name_labels,
            "datasets": [{
                "data": data[0:10],
                "backgroundColor": [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(168, 244, 205, 0.5)',
                    'rgba(170, 145, 145, 0.3)',
                    'rgba(170, 61, 61, 0.3)',
                    'rgba(58, 87, 99, 0.3)'
                ],
            }]
        }

    return jsonify(data_dict)

@app.route("/all_places.json")
def get_all_places():
    """Get JSON object with latitude and logitude of all places saved to all maps"""

    all_places = Place.query.filter().all()
    places_list = []
    for place in all_places:
        temp_dict = {}
        temp_dict['latitude'] = float(place.latitude)
        temp_dict['longitude'] = float(place.longitude)
        places_list.append(temp_dict)

    return jsonify(places_list)


@app.route('/get_places/')
def get_places():
    """Get JSON object with information about places saved to a single map"""
    
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
    """Get JSON object with information about last place saved to map"""
    
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