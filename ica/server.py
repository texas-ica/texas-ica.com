import mongoengine
import argparse

from flask import Flask
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

from ica.settings import (
    ProductionConfig, DevelopmentConfig, TestingConfig
)
from ica.views.website import website
from ica.views.social import social
from ica.models.user import User
from ica.cache import cache

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--testing', action='store_true', default=False,
                    help='start server with test settings')
parser.add_argument('-d', '--development', action='store_true', default=False,
                    help='start server with development settings')
parser.add_argument('-p', '--production', action='store_true', default=False,
                    help='start server with production settigns')
args = parser.parse_args()

if args.testing is True:
    config = TestingConfig
elif args.development is True:
    config = DevelopmentConfig
else:
    config = ProductionConfig

# Server settings
app = Flask(__name__)
app.config.from_object(config)

# Register apps
app.register_blueprint(website)
app.register_blueprint(social, url_prefix='/social')

# Database settings
db_auth = {
    'db': config.DATABASE_NAME,
    'host': config.DATABASE_HOST
}

if config is DevelopmentConfig or config is ProductionConfig:
    db_auth.update({
        'username': config.DATABASE_USER,
        'password': config.DATABASE_PASSWORD
    })

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


if __name__ == '__main__':
    app.run()
