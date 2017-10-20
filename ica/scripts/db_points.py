import os
import mongoengine

from ica.models.user import User

mongoengine.connect(
    db='heroku_b694ljx0',
    username=os.getenv('DEV_DATABASE_USER'),
    password=os.getenv('DEV_DATABASE_PASSWORD'),
    host=os.getenv('DEV_DATABASE_HOST')
)

global users
users = User.objects

def find_user(fname, lname):
    for user in users:
        if user.fname == fname and user.lname == lname:
            return user
    return None

f = open('points.txt')
data = f.read().split('\n')

for line in data:
    if line:
        fname, lname, points = line.split('\t')

        user = find_user(fname, lname)
        if user:
            user.update(set__points=points)
            print('Set {} {}\'s points to {}'.format(
                user.fname, user.lname, points
            ))
