import unittest

from base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    # Ensure that welcome page loads
    def test_welcome_route_works_as_expected(self):
        response = self.client.get('/welcome', follow_redirects=True)
        self.assertIn(b'Welcome to Flask!', response.data)

if __name__ == '__main__':
    unittest.main()
