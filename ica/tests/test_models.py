from unittest import TestCase, main

from ica.models.user import User
from ica.server import app


class TestUser(TestCase):

    def setUp(self):
        self.app = app
        self.u1 = User(
            fname='Sparkle',
            lname='Risher',
            email='sparkle@test.com',
            pwd='mangos',
            hometown='San Francisco, CA',
            major='Biology',
            year='Freshman',
            points=2000
        )
        self.u2 = User(
            fname='Blanch',
            lname='Lando',
            email='blanch@test.com',
            pwd='mangos',
            hometown='San Francisco, CA',
            major='Chemistry',
            year='Senior',
            points=3000
        )

        self.u1.save()
        self.u2.save()

    def test_password(self):
        u = User()
        password = 'default'
        u.pwd = User.hash_password(password)
        self.assertTrue(u.check_password('default'))
        self.assertFalse(u.check_password('defaultx'))

    def test_get_points_leaderboard(self):
        leaderboard = User.get_points_leaderboard(2)
        self.assertIn(self.u1, leaderboard)
        self.assertIn(self.u2, leaderboard)

        self.u1.update(set__points=0)
        leaderboard = User.get_points_leaderboard(2)
        self.assertNotIn(self.u1, leaderboard)
        self.assertIn(self.u2, leaderboard)

    def test_search(self):
        users = User.search('blanch')
        self.assertIn(self.u2, users)
        users = User.search('sparkle')
        self.assertIn(self.u1, users)

    def test_update_bio(self):
        self.u1.update_bio('I am sparkling!')
        u1 = User.objects(email='sparkle@test.com').first()
        self.assertEqual('I am sparkling!', u1.bio)

    def test_is_top_member(self):
        self.assertFalse(self.u1.is_top_member(1))
        self.assertTrue(self.u2.is_top_member(1))

    def test_follow_user(self):
        self.u1.follow_user(self.u2)

        u1 = User.objects(email='sparkle@test.com').first()
        u2 = User.objects(email='blanch@test.com').first()

        self.assertIn(self.u1, u2.followers)
        self.assertIn(self.u2, u1.following)

    def test_unfollow_user(self):
        self.u1.follow_user(self.u2)
        self.u1.unfollow_user(self.u2)
        self.assertEqual(0, len(self.u2.followers))
        self.assertEqual(0, len(self.u1.following))

    def test_is_following(self):
        self.u1.follow_user(self.u2)
        u1 = User.objects(email='sparkle@test.com').first()
        self.assertTrue(u1.is_following(self.u2))

        self.u2.follow_user(self.u1)
        u2 = User.objects(email='blanch@test.com').first()
        self.assertTrue(u2.is_following(self.u1))

        self.u1.unfollow_user(self.u2)
        u1 = User.objects(email='sparkle@test.com').first()
        self.assertFalse(u1.is_following(self.u2))

        self.u2.unfollow_user(self.u1)
        u2 = User.objects(email='blanch@test.com').first()
        self.assertFalse(u2.is_following(self.u1))

    def test_get_followers(self):
        self.u1.follow_user(self.u2)
        self.u2.follow_user(self.u1)
        self.assertIn(self.u1, self.u2.get_followers())
        self.assertIn(self.u2, self.u1.get_followers())

    def test_to_dict(self):
        exp_dict = {
            'id': '5924e4c4ac30d58629c8c667',
            'fname': 'Blanch',
            'lname': 'Lando',
            'email': 'blanch@test.com',
            'major': 'Chemistry',
            'year': 'Senior',
            'hometown': 'San Francisco, CA'
        }
        self.assertEqual(self.u2.to_dict(), exp_dict)

    def tearDown(self):
        u1 = User.objects(email='sparkle@test.com').first()
        u2 = User.objects(email='blanch@test.com').first()
        if u1 and u2:
            u1.delete()
            u2.delete()


if __name__ == '__main__':
    main()
