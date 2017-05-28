from mongoengine import (
    Document, StringField, BooleanField, IntField,
    ListField, ReferenceField
)
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ica.cache import cache


class User(Document, UserMixin):
    """ICA member account"""

    meta = {
        'indexes': [
            {
                'fields': ['$fname', '$lname'],
                'default_language': 'english'
            },
            'email',
            'pfpic_url'
        ]
    }

    # Profile information
    fname = StringField(max_length=50, required=True)
    lname = StringField(max_length=50, required=True)
    email = StringField(required=True)
    pwd = StringField(required=True)
    major = StringField(required=True)
    year = StringField(required=True)
    hometown = StringField(required=True)

    # Number of ICA points user has
    points = IntField(default=0)

    # Profile bio (optional)
    bio = StringField()

    # Hobbies
    hobbies = ListField(StringField())

    # Board member information
    board_member = BooleanField(default=False)
    board_position = StringField()

    # All users are general members, but if they pay
    # their dues, then they are active members
    general_member = BooleanField(default=True)
    active_member = BooleanField(default=False)

    # Social or service committee
    social_comm = BooleanField(default=False)
    service_comm = BooleanField(default=False)

    # Member of the week
    spotlight = BooleanField(default=False)

    # Profile picture token (stored in static/tmp/)
    pfpic_url = StringField()

    # List of following/follower users
    followers = ListField(ReferenceField('self'))
    following = ListField(ReferenceField('self'))

    @staticmethod
    def hash_password(pwd):
        return generate_password_hash(pwd)

    @staticmethod
    @cache.cached(timeout=60 * 60)
    def get_points_leaderboard(cutoff):
        fields = ['fname', 'lname', 'pfpic_url', 'year', 'points']
        leaderboard = User.objects.only(*fields).order_by(
            '-points'
        ).filter(points__gt=0)
        return leaderboard[:cutoff]

    @staticmethod
    def search(query):
        fields = ['fname', 'lname', 'followers', 'year',
                  'hometown', 'pfpic_url']
        return User.objects.only(*fields).search_text(query)

    def get_id(self):
        return str(self.id)

    def check_password(self, pwd):
        return check_password_hash(self.pwd, pwd)

    def is_top_member(self, limit):
        # leaderboard = set(User.get_points_leaderboard(limit))
        # return self in leaderboard
        return False

    def follow_user(self, user):
        user_a = User.objects(email=self.email)
        user_b = User.objects(email=user.email)
        if user_a.first().email != user_b.first().email:
            user_a.update(add_to_set__following=user)
            user_b.update(add_to_set__followers=self)

    def unfollow_user(self, user):
        user_a = User.objects(email=self.email)
        user_b = User.objects(email=user.email)
        user_a.update(pull__following=user)
        user_b.update(pull__followers=self)

    def is_following(self, user):
        return user in self.following

    def get_followers(self):
        fields = ['fname', 'lname', 'year', 'email']
        return User.objects(following=self).only(*fields)

    def update_bio(self, text):
        user = User.objects(email=self.email)
        user.update(set__bio=text)

    def get_pfpic(self):
        if self.pfpic_url:
            return self.pfpic_url
        else:
            url = 'https://s3.us-east-2.amazonaws.com/' + \
                  'icadevelopment/' + 'filler.jpg'
            return url

    def to_dict(self, extended=False):
        info = {
            'id': str(self.id),
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'major': self.major,
            'year': self.year,
            'hometown': self.hometown
        }

        if extended:
            followers = ['{} {}'.format(user.fname, user.lname) for
                         user in self.followers]
            following = ['{} {}'.format(user.fname, user.lname) for
                         user in self.following]

            info.update({
                'points': self.points,
                'bio': self.bio,
                'board_member': self.board_member,
                'board_position': self.board_position,
                'general_member': self.general_member,
                'active_member': self.active_member,
                'social_comm': self.social_comm,
                'service_comm': self.social_comm,
                'spotlight': self.spotlight,
                'pfpic_url': self.pfpic_url,
                'followers': followers,
                'following': following
            })

        return info

    def __repr__(self):
        return 'User<{} {}>'.format(self.fname, self.lname)
