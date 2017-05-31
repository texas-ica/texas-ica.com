import os
import json

from flask import Blueprint, jsonify, request
from flask_login import current_user

from ica.models.user import User
from ica.models.event import Event
from ica.models.announcement import Announcement

api = Blueprint('api', __name__)


@api.route('/board', methods=['GET'])
def get_board():
    """
    Gets information regarding the board members. This
    endpoint is used on the /board page of the website.

    URL: /board
    METHOD: GET
    URL params: None
    """

    parent = os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    ))
    path = os.path.join(parent, 'data', 'board.json')
    f = open(path, 'r')
    data = json.load(f)
    f.close()

    return jsonify({
        'data': data
    })


@api.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves a list of all registered ICA members.

    URL: /users
    METHOD: GET
    URL params:
        extended (bool): Whether the user data should contain
        extended information or only immediately important
        data, such as first name, last name, etc.
    """

    verbose = request.args.get('verbose') or False

    users = User.objects
    users = [user.to_dict(verbose) for user in users]

    return jsonify({
        'data': users
    })


@api.route('/users/search/<string:query>', methods=['GET'])
def search_users(query):
    """
    Searches members (first name and last name) through
    query string and returns relevant results. The output
    is not extended.

    URL: /users/search/<query>
    METHOD: GET
    URL params: None
    """

    users = User.objects.search_text(query)
    users = [user.to_dict() for user in users]

    return jsonify({
        'data': users
    })


@api.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    """
    Gets a single user from the database using his/her
    unique id (MongoDB ObjectID).

    URL: /users/<user_id>
    METHOD: GET
    URL params: None
    """

    user = User.objects(id=user_id).first()

    return jsonify({
        'data': user
    })


@api.route('/users/follow/', methods=['POST'])
def follow_user():
    """
    Follows a user using his/her unique id (MongoDB
    ObjectID). Success relies on authentication - if the
    request is made when the user is logged in, then the request
    will be successful, otherwise it will fail.

    URL: /users/follow/<user_id>
    METHOD: POST
    URL params: None
    """

    user_id = request.values.get('user_id')

    if hasattr(current_user, 'id'):
        user_a = User.objects(id=current_user.id).only('id').first()
        user_b = User.objects(id=user_id).only('id').first()
        if user_b:
            if user_a.id != user_b.id:
                user_a.update(add_to_set__following=user_b)
                user_b.update(add_to_set__followers=user_a)
                success = True
            else:
                success = False
    else:
        success = False

    return jsonify({
        'success': success
    })


@api.route('/users/unfollow/', methods=['POST'])
def unfollow_user():
    """
    Unfollows a user using his/her unique id (MongoDB
    ObjectID). Success relies on authentication - if the
    request is made when the user is logged in, then the request
    will be successful, otherwise it will fail.

    URL: /users/follow/<user_id>
    METHOD: POST
    URL params: None
    """

    user_id = request.values.get('user_id')

    if hasattr(current_user, 'id'):
        user_a = User.objects(id=current_user.id).only('id').first()
        user_b = User.objects(id=user_id).only('id').first()
        if user_b:
            user_a.update(pull__following=user_b)
            user_b.update(pull__followers=user_a)
            success = True
    else:
        success = False

    return jsonify({
        'success': success
    })


@api.route('/events', methods=['GET'])
def get_events():
    """
    Retrieves a list of all ICA events.

    URL: /events
    METHOD: GET
    URL params: None
    """

    events = Event.objects
    events = [event.to_dict() for event in events]

    return jsonify({
        'data': events
    })


@api.route('/announcements', methods=['GET'])
def get_announcements():
    """
    Retrieves a list of all ICA announcements.

    URL: /announcements
    METHOD: GET
    URL params: None
    """

    announcements = Announcement.objects
    announcements = [ann.to_dict() for ann in announcements]

    return jsonify({
        'data': announcements
    })
