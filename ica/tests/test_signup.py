from unittest import TestCase, main

from ica.models.user import User
from ica.server import app


class TestSignup(TestCase):

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_signup_success(self):
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

        user = User.objects(email='user@test.com')
        self.assertEqual(len(user), 1)

        user_dict = user.first().to_dict()
        keys = ['fname', 'lname', 'email', 'hometown', 'major', 'year']
        values = ['Test', 'User', 'user@test.com', 'San Francisco, CA',
                  'Computer Science', 'Freshman']

        for i in range(len(keys)):
            key, val = keys[i], values[i]
            self.assertEqual(user_dict[key], val)

    def test_incorrect_email(self):
        form = self.app.post('/signup', data={
            'fname': 'Test',
            'lname': 'User',
            'email': 'user@',
            'pwd': 'mangos',
            'pwd_confirm': 'mangos',
            'hometown': 'San Francisco, CA',
            'major': 'Computer Science',
            'year': 'Freshman'
        }, follow_redirects=True)

        html = str(form.data)
        self.assertTrue('Invalid email address.' in html)

    def test_existing_email(self):
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

        form = self.app.post('/signup', data={
            'fname': 'Second Test',
            'lname': 'User',
            'email': 'user@test.com',
            'pwd': 'mangos',
            'pwd_confirm': 'mangos',
            'hometown': 'San Francisco, CA',
            'major': 'Computer Science',
            'year': 'Freshman'
        }, follow_redirects=True)

        html = str(form.data)
        self.assertTrue('This email is already taken.'in html)

    def test_bad_password(self):
        form = self.app.post('/signup', data={
            'fname': 'Test',
            'lname': 'User',
            'email': 'user@test.com',
            'pwd': 'mango',
            'pwd_confirm': 'mangos',
            'hometown': 'San Francisco, CA',
            'major': 'Computer Science',
            'year': 'Freshman'
        }, follow_redirects=True)

        html = str(form.data)
        self.assertTrue('Passwords must match.' in html)

    def test_sanitize(self):
        self.app.post('/signup', data={
            'fname': 'TEST',
            'lname': 'user',
            'email': 'UsEr@tEsT.cOm',
            'pwd': 'mango',
            'pwd_confirm': 'mango',
            'hometown': 'San Francisco, CA',
            'major': 'Computer Science',
            'year': 'Freshman'
        }, follow_redirects=True)
        user = User.objects(email='user@test.com').first()
        self.assertEqual('Test', user.fname)
        self.assertEqual('User', user.lname)
        self.assertEqual('user@test.com', user.email)

    def tearDown(self):
        user = User.objects(email='user@test.com').first()
        if user:
            user.delete()


if __name__ == '__main__':
    main()
