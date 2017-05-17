from unittest import TestCase, main

from ica.models.user import User
from ica.utils import jsonify_response
from ica.server import app


class TestAPI(TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_users(self):
        users = User.objects
        api = self.app.get('/api/v1/users')
        resp_json = jsonify_response(api)
        self.assertEqual(len(resp_json['users']), len(users))

    def test_get_users_by_search(self):
        result = {
            'success': True,
            'users': [
                {
                    'email': 'shreydesai@test.com',
                    'fname': 'Shrey',
                    'hometown': 'Colorado, Denver',
                    'lname': 'Desai',
                    'major': 'Physics',
                    'year': 'Super Senior'
                }
            ]
        }
        api = self.app.get('/api/v1/users/shrey')
        resp_json = jsonify_response(api)
        self.assertDictEqual(resp_json, result)

    def test_get_user_by_email(self):
        result = {
            'success': True,
            'user': {
                'email': 'shreydesai@test.com',
                'fname': 'Shrey',
                'hometown': 'Colorado, Denver',
                'lname': 'Desai',
                'major': 'Physics',
                'year': 'Super Senior'
            }
        }
        api = self.app.get('/api/v1/user/shreydesai@test.com')
        resp_json = jsonify_response(api)
        self.assertDictEqual(resp_json, result)


if __name__ == '__main__':
    main()
