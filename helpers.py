from model import User, Map, Place, connect_to_db, db
import uuid

def add_user_to_database(fname, lname, email, password):
    """Add user to database"""
    user_info = User(fname=fname, lname=lname, email=email, password=password)
    db.session.add(user_info)
    db.session.commit()

def add_map_to_database(user_id, map_name, map_description):
    url_hash = uuid.uuid4() #generate random uuid (universal unique identifier) for map
    map_hex = url_hash.hex
    new_map = Map(user_id=user_id, 
                    map_name=map_name, 
                    map_description=map_description, 
                    map_url_hash=map_hex)
    db.session.add(new_map)
    db.session.commit()