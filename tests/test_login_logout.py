from flog import app
import unittest

class FlogTestCase(unittest.TestCase):

    def setUp(self):
        """Creates a test client"""
        self.app = app.test_client()

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_login_get(self):
        response_get = self.app.get('/login')
        self.assertEqual(response_get.status_code, 200)
        self.assertIn('login', response_get.data)
        self.assertIn('password', response_get.data)

    def test_login_logout(self):
        """Check login/logout"""
        response = self.app.post('/login', data=dict(
            username='root', password='root'), follow_redirects=True)
        assert b'You were logged in' in response.data

        response = self.app.get('/logout', follow_redirects=True)
        assert b'You were logged out' in response.data

        response = self.app.post('/login', data=dict(
            username='root', password='1'), follow_redirects=True)
        assert b'Incorrect login and/or password!' in response.data

        response = self.app.post('/login', data=dict(
            username='1', password='root'), follow_redirects=True)
        assert b'Incorrect login and/or password!' in response.data

if __name__ == '__main__':
    unittest.main()