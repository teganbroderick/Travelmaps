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
        self.assertIn(b'<div class="bg">', result.data)      


    def test_about_route(self):
        """Test about route"""

        result = self.client.get("/about")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>About TravelMaps</h2>', result.data) 
    

    def test_login_process(self):
        """Test login process page"""
        result = self.client.post("/login_process", 
            data={"email":"kknight@example.com", "password":"pinnacle"},
            follow_redirects="True")
        self.assertIn(b"Hello, Karl Knight!", result.data)


    def test_signup_process(self):
        """test signup process"""
        result = self.client.post("/signup_process", 
        data={"fname":"John", "lname":"Citizen", "email":"johncitizen@example.com", "password":"password!"},
        follow_redirects="True")
        self.assertIn(b"Hello, John Citizen!", result.data)   


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
        self.assertIn(b"<h2>Your Maps</h2>", result.data)  


    def test_render_map(self):
        """test user viewing one of their maps"""

        result = self.client.get("/map/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h2>San Francisco</h2>", result.data) 


    def test_logout(self):
        """test logout"""
        result = self.client.get('/logout',
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<button type="button" class="login-signup btn btn-dark" data-toggle="modal" data-target="#signup-modal">Sign Up</button>', result.data)


    def test_make_map_process(self):
        """test make map process route"""

        result = self.client.get("/make_map_process",
            query_string={"map_name":"Seattle", "map_description":"Seattle winter activities"},
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h2>Seattle</h2>", result.data)


    def test_make_map_process_already_exists(self):
        """test make map process route for trying to save a map that already exists"""

        result = self.client.get("/make_map_process",
            query_string={"map_name":"San Francisco", "map_description":"SF activities"},
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Your Maps</h2>', result.data)


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


    def test_dashboard(self):
        """test dashboard rendering for staff_user"""

        result = self.client.get('/dashboard')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Dashboard</h2>', result.data)


    def test_get_latitude_and_longitude_for_one_user(self):
        """test get_latitude_and_longitude route"""

        result = self.client.get('/get_latitude_and_longitude_for_one_user.json')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'{"latitude":37.7803399,"longitude":-122.48564420000002}', result.data)


class FlaskTestsJSON(TestCase):
    """Flask tests for JSON routes"""
    
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


    def test_get_place_statistics(self):
        """test get_place_statistics route"""
        
        result = self.client.get('/place_statistics.json')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"data":[1,1,1,1,1,1,1,1,1,1]', result.data)


    def test_get_place_type_statistics(self):
        """test get_place_type_statistics route"""

        result = self.client.get('/place_type_statistics.json')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"data":[3,2,1,1,1]', result.data)


    def test_get_latitude_and_longitude(self):
        """test get_latitude_and_longitude route"""

        result = self.client.get('/get_latitude_and_longitude.json')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'{"latitude":37.7803399,"longitude":-122.48564420000002}', result.data)


    def test_get_places(self):
        """test get_places route"""

        result = self.client.get('/get_places/',
            query_string={"map_id":3},
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'{"address":"283 King St, Newtown NSW 2042, Australia"', result.data)


    def test_get_last_place_added(self):
        """test get_places route"""
        
        result = self.client.get('/get_last_place_added/',
            query_string={"map_id":2},
            follow_redirects="True")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'"latitude":17.0438035', result.data)


if __name__ == '__main__':
    import unittest
    unittest.main()