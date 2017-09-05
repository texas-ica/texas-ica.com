import mongoengine
import os

from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_debugtoolbar import DebugToolbarExtension

from ica.api.v1 import api
from ica.views.website import website
from ica.views.social import social
from ica.views.management import management
from ica.models.user import User
from ica.cache import cache
from ica.logger import client
from ica.tasks import high_queue

# Server settings
app = Flask(__name__)
app.config.from_object(os.getenv('CONFIG'))

# Register apps
app.register_blueprint(website)
app.register_blueprint(social, url_prefix='/social')
app.register_blueprint(management, url_prefix='/management')
app.register_blueprint(api, url_prefix='/api/v1')

# Database settings
db_auth = {
    'db': app.config['DATABASE_NAME'],
    'host': app.config['DATABASE_HOST'],
    'username': app.config['DATABASE_USER'],
    'password': app.config['DATABASE_PASSWORD']
}

mongoengine.connect(**db_auth)

# Cache settings
cache.init_app(app)

# Debug toolbar settings
DebugToolbarExtension(app)

# Authentication settings
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'website.login'


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


# Error handlers
@app.errorhandler(404)
def page_not_found(error):
    header = 'Page Not Found'
    text = 'What you were looking for is just not there. ' + \
           'Go somewhere nicer.'

    if hasattr(current_user, 'id'):
        fname, lname = current_user.fname, current_user.lname
        msg = '404 ({}) from {} {}'.format(request.url, fname, lname)
    else:
        msg = '404 ({}) from Anonymous'.format(request.url)

    high_queue.enqueue(
        client.log_event,
        request.headers.get('X-Forwarded-For', request.remote_addr),
        '{} ({})'.format(msg, error)
    )

    return render_template('error.html', user=current_user,
                            header=header, text=text), 404


@app.errorhandler(500)
def internal_server_error(error):
    header = 'Internal Server Error'
    text = 'Looks like something went wrong on our end. We\'ve ' + \
           'been notified and are currently working to fix it!'

    if hasattr(current_user, 'id'):
        fname, lname = current_user.fname, current_user.lname
        msg = '500 from {} {}'.format(fname, lname)
    else:
        msg = '500 from Anonymous'

    high_queue.enqueue(
        client.log_event,
        request.headers.get('X-Forwarded-For', request.remote_addr),
        '{} ({})'.format(msg, error)
    )

    return render_template('error.html', user=current_user,
                            header=header, text=text), 500


@app.errorhandler(413)
def request_entity_error(error):
    header = 'Request Entity Too Large'
    text = 'You tried to upload a file that was too large! We only' + \
           ' support uploading photos under 500 KB, so please try again.'

    if hasattr(current_user, 'id'):
        fname, lname = current_user.fname, current_user.lname
        msg = '413 from {} {}'.format(fname, lname)
    else:
        msg = '413 from Anonymous'

    high_queue.enqueue(
        client.log_event,
        request.headers.get('X-Forwarded-For', request.remote_addr),
        '{} ({})'.format(msg, error)
    )

    return render_template('error.html', user=current_user,
                            header=header, text=text), 500
