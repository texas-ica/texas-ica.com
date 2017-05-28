import datetime

from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user

from ica.models.user import User
from ica.models.announcement import Announcement
from ica.models.event import Event
from ica.forms import ProfileForm, SearchForm
from ica.utils import (
    get_file_extension, allowed_filename, upload_photo, get_recommended_users
)
from ica.tasks import high_queue

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'tmp'

social = Blueprint('social', __name__, template_folder='templates')


@social.route('/', methods=['GET'])
@login_required
def index():
    # Get top 5 most recent announcements
    msgs_fields = ['author', 'message', 'creation_date']
    msgs = Announcement.objects.only(
        *msgs_fields
    ).order_by('-creation_date').select_related()[:5]

    # Get upcoming events
    events_fields = ['name', 'datetime', 'location', 'description',
                     'pts', 'fb_link']
    events = Event.objects.only(
        *events_fields
    ).order_by('-creation_date').select_related()

    # Filter events based on their time - if it is upcoming relative
    # to today's date, then it is included
    events = [event for event in events if
              event.datetime > datetime.datetime.now()]

    return render_template('social/index.html', **{
        'user': current_user,
        'msgs': msgs,
        'events': events
    })


@social.route('/members', methods=['GET', 'POST'])
@login_required
def members():
    member_set = None
    recommended = get_recommended_users(current_user)
    search_form = SearchForm(request.form)
    if request.method == 'POST' and search_form.validate():
        query = search_form.query.data
        fields = ['fname', 'lname', 'year', 'hometown', 'pfpic_url']
        member_set = User.objects.only(*fields).search_text(
            query
        ).order_by('fname').filter(id__ne=current_user.id)
    return render_template('social/members.html', **{
        'user': current_user,
        'search_form': search_form,
        'recommended': recommended,
        'members': member_set
    })


@social.route('/leaderboard', methods=['GET'])
@login_required
def leaderboard():
    fields = ['fname', 'lname', 'pfpic_url', 'year', 'points']
    leaderboard = User.objects.only(*fields).order_by('-points')[:10]
    leaderboard = [user for user in leaderboard if user.points > 0]
    return render_template('social/leaderboard.html', **{
        'user': current_user,
        'leaderboard': leaderboard
    })


@social.route('/followers', methods=['GET'])
@login_required
def followers():
    fields = ['fname', 'lname', 'year', 'email', 'pfpic_url']
    followers = User.objects(following=current_user.id).only(
        *fields
    ).order_by('fname')
    return render_template('social/followers.html', **{
        'user': current_user,
        'followers': followers
    })


@social.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    profile_form = ProfileForm(request.form)
    if request.method == 'POST' and profile_form.validate():
        if profile_form.bio.data:
            current_user.update(set__bio=profile_form.bio.data)
        if profile_form.hometown.data:
            current_user.update(set__hometown=profile_form.hometown.data)
        if profile_form.major.data:
            current_user.update(set__major=profile_form.major.data)
        if profile_form.year.data:
            current_user.update(set__year=profile_form.year.data)
        flash('Your profile was successfully updated!', 'success')
        return redirect(url_for('social.settings'))
    return render_template('social/settings.html', **{
        'user': current_user,
        'profile_form': profile_form
    })


@social.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_pfpic():
    if request.method == 'POST':
        # Check if request has the file part
        if 'file' not in request.files:
            flash('File not included in request', 'error')
            return redirect(url_for('social.settings'))

        # If user does not select a file, browser must also
        # submit an empty part without file part
        pic = request._get_current_object().files['file']
        if pic.filename == '':
            flash('You have not selected a picture to upload.', 'error')
            return redirect(url_for('social.settings'))

        if not allowed_filename(pic.filename, ALLOWED_EXTENSIONS):
            flash('You selected an incorrect file type. Only ' +
                  ' png, jpg, jpeg, and gif types are allowed.', 'error')
            return redirect(url_for('social.settings'))

        if pic and allowed_filename(pic.filename, ALLOWED_EXTENSIONS):
            # Generate unique picture token
            ext = get_file_extension(pic.filename)
            filename = '{}.{}'.format(current_user.id, ext)

            # Set profile picture URL
            bucket_name = 'icadevelopment'
            link = 'https://s3.us-east-2.amazonaws.com/' + bucket_name + \
                   '/' + filename
            current_user.update(set__pfpic_url=link)

            # Complete task asynchronously
            high_queue.enqueue(upload_photo, pic.read(), filename,
                               current_user.id)

            flash('Your picture will be uploaded momentarily!', 'success')
            return redirect(url_for('social.settings'))


@social.route('/follow/<string:user_id>', methods=['GET'])
@login_required
def follow_member(user_id):
    user_b = User.objects(id=user_id).only('id').first()
    if user_b:
        user_a = User.objects(id=current_user.id).only('id').first()
        if user_b.id != user_a.id:
            user_a.update(add_to_set__following=user_b)
            user_b.update(add_to_set__followers=user_a)
    return redirect(url_for('social.followers'))


@social.route('/unfollow/<string:user_id>', methods=['GET'])
@login_required
def unfollow_member(user_id):
    user_b = User.objects(id=user_id).only('id').first()
    if user_b:
        user_a = User.objects(id=current_user.id).only('id').first()
        user_a.update(pull__following=user_b)
        user_b.update(pull__followers=user_a)
    return redirect(url_for('social.followers'))
