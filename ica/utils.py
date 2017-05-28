import os
import json
import uuid
import random
from functools import wraps

from PIL import Image, ImageOps
from flask import url_for, redirect
from flask_login import current_user

from ica.models.user import User
from ica.cache import cache
from ica.images import s3


def admin_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if hasattr(current_user, 'board_member'):
            if current_user.board_member:
                return f(*args, **kwargs)
        return redirect(url_for('social.index'))
    return decorated_view


def get_file_extension(filename):
    """
    Extracts file extension from a file name
    Ex: png from pfpic.png
    """

    return filename.rsplit('.', 1)[1].lower()


def allowed_filename(filename, whitelist):
    """Determines if the file extension is in the whitelist"""

    return '.' in filename and \
           get_file_extension(filename) in whitelist


def generate_token():
    """
    DEPRECATED - use the user's MongoDB ObjectID instead

    Generates unique profile picture token
    """

    return uuid.uuid4().hex


def jsonify_response(resp):
    """
    Converts a Flask Response object to a deserialized
    JSON instance to Python object
    """

    resp_string = resp.get_data().decode('utf-8')
    return json.loads(resp_string)


@cache.memoize(timeout=60 * 60)
def get_recommended_users(user, limit=4):
    """
    Algorithm that returns a list of up to four users
    that the current user is recommended to follow
    based on personal profile settings.
    """

    fields = ['followers', 'following', 'major', 'year',
              'hometown', 'fname', 'lname']
    user = User.objects(id=user.id).only(*fields).first()

    recommended = []
    following = user.following

    # Create set of all followings the current user's
    # followings have. Take union of those sets with working
    # set to populate it.
    pool = set()
    for friend in following:
        friend_follows = set(friend.following)
        pool = pool.union(friend_follows)

    if not pool:
        return None

    # Remove current user from the set
    pool.discard(user)

    # Initialize weights for each user
    pool = list(pool)
    friends = {friend: 1.0 for friend in pool}

    # Assign weights based on matches with user
    for friend in friends:
        # Has mutual friend
        friend_follows = set(friend.following)
        my_follows = set(user.following)
        if friend_follows.intersection(my_follows):
            friends[friend] *= 0.5

        # Has same major
        if friend.major == user.major:
            friends[friend] *= 0.2

        # Has same year
        if friend.year == user.year:
            friends[friend] *= 0.2

        # Has same hometown
        if friend.hometown == user.hometown:
            friends[friend] *= 0.1

    recommended = [(friend, friends[friend])
                   for friend in friends]
    recommended = sorted(recommended, key=lambda x: x[1])
    recommended = [friend for (friend, weight) in recommended]

    return random.shuffle(recommended[:limit])


def resize_image(path):
    """
    Creates a 600x600 square thumbnail from an image
    and overwrites it in its current directory
    """

    dimension = (600, 600)
    img = Image.open(path)
    thumb = ImageOps.fit(img, dimension, Image.ANTIALIAS)
    thumb.save(path)


def upload_photo(photo_stream, filename, user_id):
    """
    Task that asynchronously downloads a user's profile picture,
    resizes it in /tmp, uploads it to S3, and updates the user's
    pfpic_url with the image's public S3 link
    """

    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(parent, 'tmp', filename)

    # Write photo byte stream to file in /tmp
    f = open(path, 'wb+')
    f.write(photo_stream)
    f.close()

    # Resize image
    resize_image(path)

    # Upload image to S3
    f = open(path, 'rb')
    bucket_name = 'icadevelopment'
    s3.upload_fileobj(
        f,
        bucket_name,
        filename,
        ExtraArgs={'ACL': 'public-read'}
    )
    f.close()

    # Remove file from tmp
    os.remove(path)
