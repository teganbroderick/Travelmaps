from server import app
from unittest import TestCase
from model import connect_to_db, db, example_data
from flask import session

class FlaskTests(TestCase):
    """Test flask routes"""

    def setUp(self):
        """Things to do before every test"""
        
        #get flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        #connect to test database
        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()


    def test_index_route(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div class="bg"></div>', result.data)

    def test_login_route(self):
        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>Login</h2>', result.data)        

    def test_about_route(self):
        result = self.client.get("/about")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h2>About Travel Maps</h2>', result.data) 

    def test_login_process(self):
        result = self.client.post("/login_process", 
            data={"email":"kknight@example.com", "password":"pinnacle"},
            follow_redirects="True")
        self.assertIn(b"Hello, Karl Knight !", result.data)

if __name__ == '__main__':
    import unittest
    unittest.main()