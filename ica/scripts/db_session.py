import os
import mongoengine

from ica.models.user import User
from ica.models.event import Event
from ica.models.announcement import Announcement

mongoengine.connect(
    db='development',
    username=os.getenv('DEV_DATABASE_USER'),
    password=os.getenv('DEV_DATABASE_PASSWORD'),
    host='mongodb://ds019471.mlab.com:19471'
)

users = User.objects
events = Event.objects
announcements = Announcement.objects
