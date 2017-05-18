import os

from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user

from ica.models.user import User
from ica.forms import BioForm, SearchForm
from ica.utils import get_file_extension, allowed_filename, generate_token

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'tmp'

social = Blueprint('social', __name__, template_folder='templates')


@social.route('/', methods=['GET'])
@login_required
def index():
    return render_template('social/index.html', **{
        'user': current_user
    })


@social.route('/members', methods=['GET', 'POST'])
@login_required
def members():
    member_set = User.objects
    search_form = SearchForm(request.form)
    if request.method == 'POST' and search_form.validate():
        query = search_form.query.data
        member_set = User.search(query)
    return render_template('social/members.html', **{
        'user': current_user,
        'search_form': search_form,
        'members': member_set.order_by('fname').filter(
            email__ne=current_user.email
        )
    })


@social.route('/leaderboard', methods=['GET'])
@login_required
def leaderboard():
    leaderboard = User.get_points_leaderboard(10)
    return render_template('social/leaderboard.html', **{
        'user': current_user,
        'leaderboard': leaderboard
    })


@social.route('/followers', methods=['GET'])
@login_required
def followers():
    followers = current_user.get_followers()
    return render_template('social/followers.html', **{
        'user': current_user,
        'followers': followers
    })


@social.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    bio_form = BioForm(request.form)
    if request.method == 'POST' and bio_form.validate():
        user = User.objects(email=current_user.email).first()
        user.update_bio(bio_form.bio.data)
        flash('Your bio was successfully updated!', 'success')
        return redirect(url_for('social.settings'))
    return render_template('social/settings.html', **{
        'user': current_user,
        'bio_form': bio_form
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
        pic = request.files['file']
        if pic.filename == '':
            flash('You have not selected a picture to upload.', 'error')
            return redirect(url_for('social.settings'))

        if not allowed_filename(pic.filename, ALLOWED_EXTENSIONS):
            flash('You selected an incorrect file type. Only ' +
                  ' png, jpg, jpeg, and gif types are allowed.', 'error')
            return redirect(url_for('social.settings'))

        if pic and allowed_filename(pic.filename):
            # Generate unique picture token
            ext = get_file_extension(pic.filename)
            filename = '{}.{}'.format(generate_token(), ext)

            # Save the picture locally
            parent = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            upload_folder = os.path.join(parent, 'static', UPLOAD_FOLDER)
            pic.save(os.path.join(upload_folder, filename))
            flash('Your picture was successfully uploaded!', 'success')

            # Update user model with picture location
            users = User.objects(email=current_user.email)
            users.update_one(set__pfpic_url=filename)

            return redirect(url_for('social.settings'))


@social.route('/follow/<string:email>', methods=['GET'])
@login_required
def follow_member(email):
    user_a = User.objects(email=current_user.email).first()
    user_b = User.objects(email=email).first()

    if user_b:
        user_a.follow_user(user_b)
    return redirect(url_for('social.followers'))


@social.route('/unfollow/<string:email>', methods=['GET'])
@login_required
def unfollow_member(email):
    user_a = User.objects(email=current_user.email).first()
    user_b = User.objects(email=email).first()
    if user_b:
        user_a.unfollow_user(user_b)
    return redirect(url_for('social.followers'))
