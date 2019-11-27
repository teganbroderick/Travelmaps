from server import app
from unittest import TestCase
from model import connect_to_db, db, example_data
from flask import session
import helpers #from helpers import <name functions>

class FlaskTests(TestCase):
    """Test flask routes"""

    def setUp(self):
        """Things to do before every test"""
        
        #get flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        #connect to test database
        connect_to_db(app, "postgresql:///testdb")
        
        db.drop_all()
        db.create_all()
        example_data()


    def test_index_route(self):
        """Test index page"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div class="bg"></div>', result.data)


    def test_login_route(self):
        """Test login route"""

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Login</h2>', result.data)        


    def test_about_route(self):
        """Test about route"""

        result = self.client.get("/about")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>About Travel Maps</h2>', result.data) 
    

    def test_login_process(self):
        """Test login process page"""
        result = self.client.post("/login_process", 
            data={"email":"kknight@example.com", "password":"pinnacle"},
            follow_redirects="True")
        self.assertIn(b"Hello, Karl Knight !", result.data)


    def test_signup_process(self):
        """test signup process"""
        result = self.client.post("/signup_process", 
        data={"fname":"John", "lname":"Citizen", "email":"johncitizen@example.com", "password":"password!"},
        follow_redirects="True")
        self.assertIn(b"Hello, John Citizen !", result.data)   


    def test_make_map(self):
        """Test make_map route"""

        result = self.client.get("/make_map")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Make New Map</h2>', result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged into session"""

    def setUp(self):
        """Things to do before every test"""
        
        #get flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "key"

        #connect to test database
        connect_to_db(app, "postgresql:///testdb")

        #define session
        with self.client as c:
            with c.session_transaction() as session:
                session['user_id'] = 1


    def test_homepage_redirect(self):
        """Test homepage redirect for when a session is active"""
        result = self.client.get("/")
        self.assertIn(b"<h2>Profile</h2>", result.data)  


    def test_render_map(self):
        """test user viewing one of their maps"""

        result = self.client.get("/map/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h3>Map Name:</h3> <p>San Francisco</p>", result.data) 


    def test_logout(self):
        """test logout"""
        result = self.client.get('/logout',
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<input type="submit" value="Login/Sign Up">', result.data)


    def test_make_map_process(self):
        """test make map process route"""

        result = self.client.get("/make_map_process",
            query_string={"map_name":"Seattle", "map_description":"Seattle winter activities"},
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h3>Map Name:</h3> <p>Seattle</p>", result.data)


    def test_make_map_process_already_exists(self):
        """test make map process route for trying to save a map that already exists"""

        result = self.client.get("/make_map_process",
            query_string={"map_name":"San Francisco", "map_description":"SF activities"},
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Make New Map</h2>', result.data)


    def test_save_location(self):
        """test saving a place to a map"""

        result = self.client.post("/map/1/save",
            data={"title":"Fleamarket at Mauerpark", 
                    "address":"Bernauer Str. 63-64, 13355 Berlin, Germany",
                    "website":"http://www.flohmarktimmauerpark.de/",
                    "types":"[tourist_attraction,point_of_interest,establishment]",
                    "google_places_id":"ChIJCydkxPlRqEcRAVlBoABIR_0",
                    "latitude":"52.54123999999999",
                    "longitude":"13.402435100000048",
                    "user_notes":"Good place to buy old stuff"},
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<a class="place-name" href="/" data-name="Fleamarket at Mauerpark">Fleamarket at Mauerpark</a>', result.data)


    def test_delete_location(self):
        """Test deleting a place from a map"""

        result = self.client.post('/map/1/delete',
            data={"google_places_id":"ChIJszBPbLWHhYARfrlLxEb3GuA"},
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertNotIn(b'<a class="place-name" href="/" data-name="Sutro Baths">Sutro Baths</a>', result.data)


    def test_share_map(self):
        """Test share map route"""

        result = self.client.get('/share_map/0c38abd239da4782b1510e57d0eb49d')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<button type="button" class="get-shareable-link" data-toggle="modal" data-target="#share-link-modal">', result.data)





if __name__ == '__main__':
    import unittest
    unittest.main()