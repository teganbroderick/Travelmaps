from model import User, Map, Place, connect_to_db, db
import uuid
from flask import session, flash

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


def make_place_type_dictionary(all_place_types):
    """ Make dictionary from list of all place types. 
        Dictionary keys = place types, values = number of times place type 
        has been added to all maps
    """

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


def get_data_and_labels_for_chart(place_type_dictionary):
    """get sorted lists of values and keys from input dictionary"""

    data = sorted(place_type_dictionary.values(), reverse=True) #sort dict on values
    labels = sorted(place_type_dictionary, key=place_type_dictionary.__getitem__, reverse=True) #get key associated with sorted values

    return [data, labels]


def make_data_dict_for_donut_chart(data_labels_list):
    """Make a data_dictionary to pass through into chart.js donut chart"""

    data_dict = {
            "labels": data_labels_list[1][0:5], #getting top 5 place types, so slicing from 0 - 5
            "datasets": [
                {
                    "data": data_labels_list[0][0:5],
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

    return data_dict


def make_place_dictionary(all_places):
    """ Make dictionary from list of place names/ places id tuples. 
        Dictionary keys = place names, values = number of times place 
        has been added to all maps
    """
    place_dictionary = {} 
    for place in all_places:
        if place_dictionary.get(place) == None:
            place_dictionary[place] = 1
        else:
            place_dictionary[place] += 1 
    
    return place_dictionary


def get_place_names(data_labels_list):
    """Create list of place name labels from labels tuple in data_labels_list"""

    labels = data_labels_list[1]
    name_labels = []
    for i in range(0,10):
        name_only = labels[i][0]
        name_labels.append(name_only)
    return name_labels


def make_data_dict_for_bar_chart(data_labels_list, place_names_list):
    """Make a data_dictionary to pass through into chart.js bar chart"""

    data_dict = {
        "labels": place_names_list,
        "datasets": [{
            "data": data_labels_list[0][0:10],
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

    return data_dict


def get_latitude_and_longitude_list(all_places):
    """Return list of dictionaries containing latitude and longitude of all places"""

    places_list = []
    for place in all_places:
        temp_dict = {}
        temp_dict['latitude'] = float(place.latitude)
        temp_dict['longitude'] = float(place.longitude)
        places_list.append(temp_dict)

    return places_list


def list_of_places_on_map(places_on_map):
    """Return list of dictionaries containing attributes about all places saved to a map"""
    
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

    return places_list

def last_place_added_dict(all_places_on_map):
    """Return  dictionary containing latitude and longitude of last place saved to a map
        If no place has been added to map, use latitude and longitude of San Francisco.
    """

    last_place_added_dict = {}

    if all_places_on_map != []: #if there are places saved to the map
        last_place_added = all_places_on_map[-1]
        last_place_added_dict['latitude'] = float(last_place_added.latitude)
        last_place_added_dict['longitude'] = float(last_place_added.longitude)
    else:
        last_place_added_dict['latitude'] = float(37.7749295) 
        last_place_added_dict['longitude'] = float(-122.41941550000001)

    return last_place_added_dict


def get_all_places_on_one_users_maps(all_maps):
    """Return list of place objects for all palces saved to all of one user's maps"""

    places_object_list = []

    for map1 in all_maps:
        places = Place.query.filter(Place.map_id == map1.map_id).all()
        for place in places:
            places_object_list.append(place)

    return places_object_list



