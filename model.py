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




