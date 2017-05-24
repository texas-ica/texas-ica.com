import mongoengine
import os

from flask import Flask
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

from ica.api.v1 import api
from ica.views.website import website
from ica.views.social import social
from ica.views.management import management
from ica.models.user import User
from ica.cache import cache

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
