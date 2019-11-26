from server import app
from unittest import TestCase
from model import connect_to_db, db, example_data
from flask import session
import helpers

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


    def test_make_map(self):
        """Test make_map route"""

        result = self.client.get("/make_map")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Make New Map</h2>', result.data)

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

    # def test_logout(self):
    #     result = self.client.get('/logout')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'<div class="bg"></div>', result.data)

    # def test_make_map_process(self):
    #     #Work in progress - needs session info
    #     result = self.client.post("/make_map_process",
    #         data={"map_name":"Seattle", "map_description":"Seattle winter activities"},
    #         follow_redirects="True")
    #     # self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"<h3>Map Name:</h3> <p> Seattle </p>", result.data)




if __name__ == '__main__':
    import unittest
    unittest.main()