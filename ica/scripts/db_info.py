import os
import mongoengine

from ica.models.user import User
from ica.models.event import Event
from ica.models.announcement import Announcement

mongoengine.connect(
    db='heroku_b694ljx0',
    username=os.getenv('DEV_DATABASE_USER'),
    password=os.getenv('DEV_DATABASE_PASSWORD'),
    host=os.getenv('DEV_DATABASE_HOST')
)

users = User.objects
events = Event.objects
announcements = Announcement.objects

for user in users:
    print('{}\t{}'.format(user.fname + ' ' + user.lname, user.email))
