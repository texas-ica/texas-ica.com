from mongoengine import (
    Document, StringField, BooleanField, IntField,
    ListField, ReferenceField
)
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(Document, UserMixin):
    """ICA member account"""

    meta = {
        'indexes': [{'fields': ['$fname', '$lname'],
                    'default_language': 'english'}]
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
    def get_points_leaderboard(cutoff):
        leaderboard = sorted(User.objects, key=lambda x: x.points,
                             reverse=True)
        leaderboard = leaderboard[:cutoff]
        return [x for x in leaderboard if x.points != 0]

    @staticmethod
    def search(query):
        return User.objects.search_text(query)

    def get_id(self):
        return str(self.id)

    def check_password(self, pwd):
        return check_password_hash(self.pwd, pwd)

    def is_top_member(self, limit):
        leaderboard = set(User.get_points_leaderboard(limit))
        return self in leaderboard

    def follow_user(self, user):
        user_a = User.objects(email=self.email)
        user_b = User.objects(email=user.email)
        if user_a is not user_b:
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
        return User.objects(following=self)

    def update_bio(self, text):
        user = User.objects(email=self.email)
        user.update(set__bio=text)

    def get_pfpic(self):
        pass

    def to_dict(self, extended=False):
        info = {
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'major': self.major,
            'year': self.year,
            'hometown': self.hometown
        }

        if extended:
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
                'followers': self.followers,
                'following': self.following
            })

        return info

    def __repr__(self):
        return 'User<{} {}>'.format(self.fname, self.lname)
