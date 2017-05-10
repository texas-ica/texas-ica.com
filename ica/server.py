from flask import Flask
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
import mongoengine

from ica.settings import DevelopmentConfig
from ica.views.website import website
from ica.views.social import social
from ica.models.user import User

# Server settings
app = Flask(__name__)
config = DevelopmentConfig
app.config.from_object(config)

# Register apps
app.register_blueprint(website)
app.register_blueprint(social, url_prefix='/social')

# Database settings
mongoengine.connect(
    db=config.DATABASE_NAME,
    username=config.DATABASE_USER,
    password=config.DATABASE_PASSWORD,
    host=config.DATABASE_HOST
)

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
    app.run(debug=True)
