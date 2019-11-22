from server import app
from unittest import TestCase

class FlaskTests(TestCase):
    """Test flask routes"""

    def setUp(self):
        """Things to do before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_flask_route(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div class="bg"></div>', result.data)


if __name__ == '__main__':
    import unittest
    unittest.main()