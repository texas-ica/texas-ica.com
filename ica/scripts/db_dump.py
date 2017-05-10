import os
import random
import mongoengine

from ica.models.user import User

mongoengine.connect(
    db='development',
    username=os.getenv('DEV_DATABASE_USER'),
    password=os.getenv('DEV_DATABASE_PASSWORD'),
    host='mongodb://ds019471.mlab.com:19471'
)

f = open('data/members.txt', 'r')
members = f.read().strip().split('\n')

g = open('data/cities.txt', 'r')
cities = g.read().strip().split('\n')
cities = [c.split('\t') for c in cities]
cities = ['{}, {}'.format(x, y) for x, y in cities]

h = open('data/majors.txt', 'r')
majors = h.read().strip().split('\n')

status = ['Freshman', 'Sophomore', 'Junior',
          'Senior', 'Super Senior']

for i, member in enumerate(members):
    print('Creating {}/{}'.format(i + 1, len(members)))

    # Randomize data
    fname, lname = member.split(' ')
    email = '{}{}@test.com'.format(fname.lower(), lname.lower())
    pwd = User.hash_password('test')
    hometown = random.choice(cities)
    major = random.choice(majors)
    year = random.choice(status)
    points = random.randrange(200)

    # Create user schema
    u = User(fname=fname, lname=lname, email=email, pwd=pwd,
             hometown=hometown, major=major, year=year, points=points)
    u.save()

    # Follow random users
    users = list(User.objects)
    random.shuffle(users)
    follows = random.randrange(5)
    follow_list = list(users)[:follows]
    for person in follow_list:
        u.follow_user(person)
