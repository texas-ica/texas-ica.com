from flask import request
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField, IntegerField, BooleanField,
    DecimalField, DateField
)
from wtforms.validators import (
    DataRequired, Length, EqualTo, Email, optional
)

from ica.models.user import User
from ica.logger import client
from ica.tasks import low_queue


class SignUpForm(FlaskForm):
    """ICA Social user sign up form"""

    fname = StringField('First Name', [DataRequired()])
    lname = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [DataRequired(), Email()])
    pwd = PasswordField('Password', [DataRequired()])
    pwd_confirm = PasswordField('Confirm Password', [
        DataRequired(), EqualTo('pwd', message='Passwords must match.')
    ])
    hometown = StringField('Hometown', [DataRequired()])
    major = StringField('Major', [DataRequired()])
    year = SelectField('Year', [DataRequired()], choices=[
        ('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'), ('Senior', 'Senior'),
        ('Super Senior', 'Super Senior')
    ])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        # Check whether this email is already taken by
        # another user in the database
        existing_user = User.objects(email=self.email.data)
        if existing_user:
            self.email.errors.append('This email is already taken.')
            return False

        return True


class LoginForm(FlaskForm):
    """ICA Social user login form"""

    email = StringField('Email', [DataRequired(), Email()])
    pwd = PasswordField('Password', [DataRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        # Check if user exists in the database
        existing_user = User.objects(email=self.email.data).first()
        if not existing_user:
            msg = 'The email you\'ve entered doesn\'t match ' + \
                  ' any existing account.'
            self.email.errors.append(msg)

            low_queue.enqueue(
                client.log_event,
                request.headers.get('X-Forwarded-For', request.remote_addr),
                'Anonymous entered incorrect email \'{}\''.format(
                    self.email.data
                )
            )

            return False

        # Check if user's password is correct
        if not existing_user.check_password(self.pwd.data):
            msg = 'The password you\'ve entered is incorrect.'
            self.pwd.errors.append(msg)

            low_queue.enqueue(
                client.log_event,
                request.headers.get('X-Forwarded-For', request.remote_addr),
                'Anonymous entered incorrect password \'{}\''.format(
                    self.pwd.data
                )
            )

            return False

        return True


class ProfileForm(FlaskForm):
    """Form to update profile settings"""

    bio = StringField('Bio')
    hometown = StringField('Hometown')
    major = StringField('Major')
    year = SelectField('Year', choices=[
        ('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'), ('Senior', 'Senior'),
        ('Super Senior', 'Super Senior')
    ])


class SearchForm(FlaskForm):
    """Form used to query for users on the members page"""

    query = StringField('Query')


class DatabaseEditForm(FlaskForm):
    """
    Comprehensive form used to edit user settings - used on
    the board member management page
    """

    fname = StringField('First Name')
    lname = StringField('Last Name')
    email = StringField('Email')
    hometown = StringField('Hometown')
    major = StringField('Major')
    year = SelectField('Year', choices=[
        ('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'), ('Senior', 'Senior'),
        ('Super Senior', 'Super Senior')
    ])
    points = IntegerField('Points', [optional()])
    board_member = BooleanField('Board Member')
    board_position = StringField('Board Position')
    general_member = BooleanField('General Member')
    active_member = BooleanField('Active Member')
    spotlight = BooleanField('Spotlight')


class AnnouncementForm(FlaskForm):
    """
    Form to create an announcement - shows up on the ICA
    social network oveview page
    """

    text = StringField('Announcement Message', [
        Length(min=1, max=300), DataRequired()
    ])


class EventForm(FlaskForm):
    """
    Form to create an event - shows up on the ICA social
    network overview page
    """

    name = StringField('Name', [DataRequired()])
    datetime = DateField('Date (ex: 05/20/2017)',
                         [DataRequired()], format='%m/%d/%Y')
    location = StringField('Location', [DataRequired()])
    description = StringField('Description', [DataRequired()])
    pts = DecimalField('Points per Hour', [DataRequired()])
    fb_link = StringField('Facebook Event Link (optional)')
