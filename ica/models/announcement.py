import datetime

from mongoengine import (
    Document, StringField, DateTimeField,
    ReferenceField, ListField
)

from ica.models.user import User


class Announcement(Document):
    """
    Announcement that appears on the ICA social
    network dashboard
    """

    # Author of the announcement (this needs
    # to be a board member)
    author = ReferenceField(User, required=True)

    # Announcement text
    message = StringField(required=True)

    # When the announcement was created
    creation_date = DateTimeField(default=datetime.datetime.now)

    # Users that like the announcement
    likes = ListField(ReferenceField(User))

    def __repr__(self):
        return 'Announcement<{}, {}>'.format(
            self.author, self.message
        )

    def to_dict(self):
        return {
            'author': self.author,
            'message': self.message,
            'likes': self.likes
        }
