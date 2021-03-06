# tests/test_users.py


import unittest

from flask_login import current_user
from flask import request

from base import BaseTestCase
from project import bcrypt
from project.models import User


class TestUser(BaseTestCase):

# Ensure id is correct for the current/logged in user
    def test_get_by_id(self):
        with self.client:
            self.client.post('/login', data=dict(
                username="admin", password='admin'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)

    # Ensure given password is correct after unhashing
    def test_check_password(self):
        user = User.query.filter_by(email='ad@min.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))



class GuestTests(BaseTestCase):

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn(b'Please login', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username="guest", password="guest"),
                follow_redirects=True
            )
            self.assertIn(b'You were logged in', response.data)
            self.assertTrue(current_user.name == "guest")
            self.assertTrue(current_user.is_active)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid username or password.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="guest", password="guest"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out', response.data)
            self.assertFalse(current_user.is_active)

    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_reduced_access(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="guest", password="guest"),
                follow_redirects=True
            )
            response = self.client.get('/guest', follow_redirects=True)
            self.assertIn(b'Welcome Guest!', response.data)
            response = self.client.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 403)

class AdminTests(BaseTestCase):
    def test_full_access(self):
        with self.client:
            self.client.post('/login',
                             data=dict(username='admin', password='admin'),
                             follow_redirects=True)
            response = self.client.get('/', follow_redirects=True)
            self.assertIn(b'You are an admin', response.data)
            response = self.client.get('/guest', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
