from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email

from ica.models.user import User


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
            return False

        # Check if user's password is correct
        if not existing_user.check_password(self.pwd.data):
            msg = 'The password you\'ve entered is incorrect.'
            self.pwd.errors.append(msg)
            return False

        return True


class BioForm(FlaskForm):
    """Form to update profile bio/description"""

    bio = StringField('Bio')


class SearchForm(FlaskForm):
    """Form used to query for users on the members page"""

    query = StringField('Query')
