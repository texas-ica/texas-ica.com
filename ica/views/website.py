import os
import json

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session
)
from flask_login import login_user, logout_user, current_user

from ica.models.user import User
from ica.forms import SignUpForm, LoginForm

website = Blueprint('website', __name__, template_folder='templates')


@website.route('/', methods=['GET'])
def index():
    return render_template('website/index.html', **{
        'user': current_user
    })


@website.route('/blog', methods=['GET'])
def blog():
    return render_template('website/blog.html', **{
        'user': current_user
    })


@website.route('/board', methods=['GET'])
def board():
    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(parent, 'data', 'board.json')
    stream = open(path, 'r')
    data = json.load(stream)
    stream.close()
    sorted_data = sorted(data.items(), key=lambda i: int(i[0]))
    return render_template('website/board.html', **{
        'user': current_user,
        'data': sorted_data
    })


@website.route('/faq', methods=['GET'])
def faq():
    return render_template('website/faq.html', **{
        'user': current_user
    })


@website.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        u = User(
            fname=form.fname.data.capitalize(),
            lname=form.lname.data.capitalize(),
            email=form.email.data.lower(),
            pwd=User.hash_password(form.pwd.data),
            hometown=form.hometown.data,
            major=form.major.data,
            year=form.year.data
        )
        u.save()
        flash('Head over to the login page to sign in!')
        return redirect(url_for('website.signup'))
    return render_template('website/signup.html', **{
        'user': current_user,
        'form': form
    })


@website.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('social.index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects(email=form.email.data).first()
        login_user(user)
        return redirect(url_for('social.index'))
    return render_template('website/login.html', **{
        'user': current_user,
        'form': form
    })


@website.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('website.index'))
