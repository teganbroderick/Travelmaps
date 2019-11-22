from server import app
from unittest import TestCase

class FlaskTests(TestCase):
    """Test flask routes"""

    def setUp(self):
        """Things to do before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True


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

if __name__ == '__main__':
    import unittest
    unittest.main()