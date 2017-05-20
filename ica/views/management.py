from flask import (
    Blueprint, render_template, request, redirect, flash, url_for
)
from flask_login import login_required, current_user
from mongoengine.errors import ValidationError

from ica.models.user import User
from ica.models.announcement import Announcement
from ica.models.event import Event
from ica.forms import DatabaseEditForm, AnnouncementForm, EventForm

management = Blueprint('management', __name__,
                       template_folder='management')


@management.route('/', methods=['GET'])
@login_required
def index():
    return render_template('management/index.html', **{
        'user': current_user
    })


@management.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    members = User.objects.only('fname', 'lname', 'year', 'pfpic_url')
    return render_template('management/edit.html', **{
        'user': current_user,
        'members': members.order_by('fname')
    })


@management.route('/edit_user/<string:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    try:
        focus = User.objects(id=user_id).first()
        form = DatabaseEditForm(request.form)
        if request.method == 'POST' and form.validate():
            if form.fname.data:
                focus.update(set__fname=form.fname.data)
            if form.lname.data:
                focus.update(set__lname=form.lname.data)
            if form.email.data:
                focus.update(set__email=form.email.data)
            if form.hometown.data:
                focus.update(set__hometown=form.hometown.data)
            if form.major.data:
                focus.update(set__major=form.major.data)
            if form.year.data:
                focus.update(set__year=form.year.data)
            if form.points.data:
                focus.update(set__points=form.points.data)
            if form.board_member.data:
                focus.update(set__board_member=form.board_member.data)
            if form.general_member.data:
                focus.update(set__general_member=form.general_member.data)
            if form.active_member.data:
                focus.update(set__active_member=form.active_member.data)
            if form.spotlight.data:
                focus.update(set__spotlight=form.spotlight.data)
            flash('{} {}\'s profile was updated'.format(
                focus.fname, focus.lname
            ))
            return redirect(url_for('management.edit_user',
                                    user_id=user_id))

    except ValidationError:
        focus = None
    return render_template('management/edit_user.html', **{
        'user': current_user,
        'focus': focus,
        'form': form
    })


@management.route('/points', methods=['GET', 'POST'])
@login_required
def points():
    return render_template('management/points.html', **{
        'user': current_user
    })


@management.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():
    fields = ['message', 'creation_date']
    msgs = Announcement.objects(author=current_user.id).only(
        *fields
    ).order_by('creation_date').select_related()
    form = AnnouncementForm(request.form)
    if request.method == 'POST' and form.validate():
        announcement = Announcement(
            author=current_user.id,
            message=form.text.data
        )
        announcement.save()
        flash('Your announcement was posted on the overview page!')
        return redirect(url_for('management.announcements'))
    return render_template('management/announcements.html', **{
        'user': current_user,
        'msgs': msgs,
        'form': form
    })


@management.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    fields = ['name', 'datetime', 'location', 'pts']
    events = Event.objects(author=current_user.id).only(
        *fields
    ).order_by('datetime').select_related()
    form = EventForm(request.form)
    if request.method == 'POST' and form.validate():
        fields = {
            'name': form.name.data,
            'datetime': form.datetime.data,
            'location': form.location.data,
            'description': form.description.data,
            'pts': form.pts.data,
            'author': current_user.id
        }

        if form.fb_link.data:
            fields.update({'fb_link': form.fb_link.data})

        event = Event(**fields)
        event.save()

        flash('This announcement will show up on the' +
              ' member overview page.')
        return redirect(url_for('management.events'))
    return render_template('management/events.html', **{
        'user': current_user,
        'events': events,
        'form': form
    })
