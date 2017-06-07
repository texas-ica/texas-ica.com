from mongoengine import (
    Document, StringField, IntField, DateTimeField,
    ListField, ReferenceField
)

from ica.models.user import User


class Event(Document):

    # Name of the event
    name = StringField(required=True)

    # Date and time event is being held
    # Format: %Y-%m-%d (time isn't used)
    datetime = DateTimeField(required=True)

    # Where the event is taking place
    location = StringField(required=True)

    # Description of event - most likely copy/pasted
    # from its Facebook description
    description = StringField(required=True)

    # Points per hour for members
    pts = IntField(min_value=0, required=True)

    # Link to QR code
    qr_code = StringField()

    # Unique event code
    code = StringField()

    # Link to Facebook event - might not be relevant for
    # ad-hoc events like 'Flash Study Hours'
    fb_link = StringField()

    # Board member in charge of the event
    author = ReferenceField(User)

    # Members that attended the event
    attended = ListField(ReferenceField(User))

    def __repr__(self):
        return 'Event<{}>'.format(self.name)

    def to_dict(self):
        author = self.author.to_dict()
        attended = [user.to_dict() for user in self.attended]

        return {
            'name': self.name,
            'datetime': self.datetime,
            'location': self.location,
            'description': self.description,
            'pts': str(self.pts),
            'fb_link': self.fb_link,
            'author': author,
            'attended': attended
        }
