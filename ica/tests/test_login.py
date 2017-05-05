from unittest import TestCase, main

from ica.models.user import User
from ica.server import app


class TestLogin(TestCase):

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

        # create test user
        self.app.post('/signup', data={
            'fname': 'Test',
            'lname': 'User',
            'email': 'user@test.com',
            'pwd': 'mangos',
            'pwd_confirm': 'mangos',
            'hometown': 'San Francisco, CA',
            'major': 'Computer Science',
            'year': 'Freshman'
        }, follow_redirects=True)

    def test_incorrect_email(self):
        form = self.app.post('/login', data={
            'email': 'user@test.net',
            'pwd': 'mangos'
        }, follow_redirects=True)

        html = str(form.data)
        html = html.replace('&#39;', '\'')
        msg = 'The email you\'ve entered doesn\'t match ' + \
              ' any existing account.'

        self.assertTrue(msg in html)

    def test_incorrect_password(self):
        form = self.app.post('/login', data={
            'email': 'user@test.com',
            'pwd': 'mango'
        }, follow_redirects=True)

        html = str(form.data)
        html = html.replace('&#39;', '\'')
        msg = 'The password you\'ve entered is incorrect.'
        self.assertTrue(msg in html)

    def tearDown(self):
        user = User.objects(email='user@test.com').first()
        if user:
            user.delete()


if __name__ == '__main__':
    main()
