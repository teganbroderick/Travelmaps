from flask_sqlalchemy import SQLAlchemy

# Instantiate a SQLAlchemy object
db = SQLAlchemy()

class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    staff_user = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        """Return a human-readable representation of a user"""

        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}>"

class Map(db.Model):
    """Data model for a map."""

    __tablename__ = "maps"

    map_id = db.Column(db.Integer, 
                        primary_key=True,   
                        autoincrement=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))
    map_name = db.Column(db.String(50), nullable=False)
    map_description = db.Column(db.String(100), nullable=True)
    map_url_hash = db.Column(db.String(32), nullable=False)

    #***********
    user = db.relationship("User", backref="maps")
    place = db.relationship("Place", backref="maps")
    #***********

    def __repr__(self):
        """Return a human-readable representation of a map"""

        return f"<Map map_id={self.map_id} user_id={self.user_id} map_name={self.map_name}>"


class Place(db.Model):
    """Data model for a place."""

    __tablename__ = "places"

    place_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    map_id = db.Column(db.Integer, 
                        db.ForeignKey('maps.map_id'))
    google_place_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    website = db.Column(db.String(200), nullable=False)
    place_types = db.Column(db.String(100), nullable=False)
    google_places_id = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    user_notes = db.Column(db.String(300), nullable=False)
    place_active = db.Column(db.Boolean, default=True, nullable=False)
    

    def __repr__(self):
        """Return a human-readable representation of a place"""

        return f"<Place place_id={self.place_id} map_id={self.map_id} google_place_name={self.google_place_name} address={self.address} website={self.website} place_types={self.place_types} google_places_id={self.google_places_id} latitude={self.latitude} longitude={self.longitude} user_notes={self.user_notes} place_active={self.place_active}>"


def example_data():
    """Create some example data"""
    
    #Example users
    gwen = User(fname="Gwendolyn", lname="Murray", email="gwendolyn.murray@example.com", password="kikimora", staff_user=True)
    jesse = User(fname="Jesse", lname="Wilson", email="jwilson@example.com", password="lola")
    karl = User(fname="Karl", lname="Knight", email="kknight@example.com", password="pinnacle")

    #Example maps
    map1 = Map(user=gwen, map_name="San Francisco", map_description="SF activities", map_url_hash="0c38abd239da4782b1510e57d0eb49d")
    map2 = Map(user=jesse, map_name="Sydney", map_description="Sydney summer", map_url_hash="e514f0af375b4343930437cbba9793c3")
    map3 = Map(user=gwen, map_name="Mexico City", map_description="CDMX", map_url_hash="c3e6bbf7f9ab40248360934ff41104fd")

    #Example places
    place1 = Place(maps=map1, 
                    google_place_name="Trad'r Sam", 
                    address="6150 Geary Blvd, San Francisco, CA 94121, United States", 
                    website="website not available", 
                    place_types="bar,point_of_interest,establishment", 
                    google_places_id="ChIJC5_zVw-HhYARet1rQr-DRl0", 
                    latitude="37.7803399", 
                    longitude="-122.48564420000002", 
                    user_notes="I've been to a good amount of tiki bars in San Francisco, but always find myself coming back to Trad'r Sam's", 
                    place_active=True)
    place2 = Place(maps=map1, 
                    google_place_name="Sutro Baths", 
                    address="1004 Point Lobos Ave, San Francisco, CA 94121, USA", 
                    website="https://www.nps.gov/goga/planyourvisit/cliff-house-sutro-baths.htm", 
                    place_types="tourist_attraction,point_of_interest,establishment", 
                    google_places_id="ChIJszBPbLWHhYARfrlLxEb3GuA", 
                    latitude="37.7804369", 
                    longitude="-122.51369349999999", 
                    user_notes="Ruins of some former indoor baths/pools. Great place to start out on a hike around lands end.", 
                    place_active=True)
    place3 = Place(maps=map2, 
                    google_place_name="Newtown Pies", 
                    address="283 King St, Newtown NSW 2042, Australia", 
                    website="http://www.facebook.com/Newtown-Pies-1544119209140408/", 
                    place_types="bakery,restaurant,food,point_of_interest,store,establishment", 
                    google_places_id="ChIJw2dSRjGwEmsRbUUCEXKvL0Q", 
                    latitude="-33.8963689", longitude="151.1798463", 
                    user_notes="Some of the best meat pies around", 
                    place_active=True)
    place4 = Place(maps=map3, 
                    google_place_name="Taronga Zoo Sydney ", 
                    address="Bradleys Head Rd, Mosman NSW 2088, Australia", 
                    website="https://taronga.org.au/taronga-zoo", 
                    place_types="zoo,tourist_attraction,point_of_interest,establishment", 
                    google_places_id="ChIJq6qqWiSsEmsRJuIpepyEua4", 
                    latitude="-33.8435473", longitude="151.2413418", 
                    user_notes="Zoo with a lovely view of the harbour ", 
                    place_active=True)
    place5 = Place(maps=map3, 
                    google_place_name="Xochimilco", 
                    address="Xochimilco, CDMX, Mexico", 
                    website="website not available ", 
                    place_types="administrative_area_level_3,political", 
                    google_places_id="ChIJo97obYwDzoURhFO92h_3eZs", 
                    latitude="19.2572314", longitude="-99.10296640000001", 
                    user_notes="Unesco world heritage site with floating barges", 
                    place_active=True)
    place6 = Place(maps=map3, 
                    google_place_name="Museo Nacional de Antropología", 
                    address="Av. Paseo de la Reforma s/n, Polanco, Bosque de Chapultepec I Secc, Miguel Hidalgo, 11560 Ciudad de México, CDMX, Mexico", 
                    website="https://www.mna.inah.gob.mx/", 
                    place_types="museum,tourist_attraction,point_of_interest,establishment", 
                    google_places_id="ChIJScjIILQB0oURJMVub-MaI4Q", 
                    latitude="19.4260032", 
                    longitude="-99.18627859999998", 
                    user_notes="Great collection, beautiful building", 
                    place_active=True)

    db.session.add_all([gwen, jesse, karl, map1, map2, map3, place1, place2, place3, place4, place5, place6])
    db.session.commit()
    

def connect_to_db(app, db_uri="postgresql:///travelmaps"):
    """Connect the database to the Flask app"""

    # Configure to use the database.
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")




