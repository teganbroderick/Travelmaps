from model import User, Map, Place, connect_to_db, db
import uuid

def add_user_to_database(fname, lname, email, password):
    """Add user to database"""
    user_info = User(fname=fname, lname=lname, email=email, password=password)
    db.session.add(user_info)
    db.session.commit()

def user_login(email):
    """Add user to session, return user object"""
    user = User.query.filter_by(email=email).first() #get user object
    session['user_id'] = user.user_id #add user to session  
    flash("Logged in!")
    return user

def add_map_to_database(user_id, map_name, map_description):
    """Add map to database"""
    url_hash = uuid.uuid4() #generate random uuid (universal unique identifier) for map
    map_hex = url_hash.hex
    new_map = Map(user_id=user_id, 
                    map_name=map_name, 
                    map_description=map_description, 
                    map_url_hash=map_hex)
    db.session.add(new_map)
    db.session.commit()

def add_place_to_database(map_id, google_place_name, address, website, place_types, google_places_id, latitude, longitude, user_notes):
    """Add place to database"""
    new_place = Place(map_id=map_id, 
                    google_place_name=google_place_name,
                    address=address,
                    website=website,
                    place_types=place_types,
                    google_places_id=google_places_id,
                    latitude=latitude, 
                    longitude=longitude, 
                    user_notes=user_notes)
    db.session.add(new_place)
    db.session.commit()

def delete_place_from_map(map_id, place_to_delete_id):
    """Change place from place_active=True to place_active=False in places table"""
    
    place_to_delete = Place.query.filter(Place.google_places_id == place_to_delete_id, Place.map_id == map_id).first()
    #change place_active to false for place_to_delete. Place will no longer be rendered on the map.
    place_to_delete.place_active = False
    db.session.commit() 

def user_stats():
    """Get user statistics for display on internal dashboard page"""

    stats_dictionary = {}
    stats_dictionary['total_users'] = len(User.query.filter().all())
    stats_dictionary['total_maps']= len(db.session.query(Map.map_id).all())
    stats_dictionary['total_places_mapped'] = len(Place.query.filter().all())
    stats_dictionary['avg_places_mapped'] = round(stats_dictionary['total_places_mapped'] / stats_dictionary['total_maps'], 2)
    stats_dictionary['avg_maps_per_user'] = round(stats_dictionary['total_maps'] / stats_dictionary['total_users'], 2)
    
    return stats_dictionary

def make_place_dictionary(all_place_types):
    """Make dictionary from list of all place types. 
    Dictionary keys = place types, values = number of times place type 
    has been added to all maps"""

    place_type_dictionary = {} 
    for place in all_place_types:
        #split string in tuple into individual place types
        types = place[0].split(",") 
        #get first place type tag from each place, make dictionary with place types and count
        if place_type_dictionary.get(types[0]) == None:
            place_type_dictionary[types[0]] = 1
        else:
            place_type_dictionary[types[0]] += 1

    return place_type_dictionary

