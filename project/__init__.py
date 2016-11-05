#################
#### imports ####
#################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal
import os


################
#### config ####
################

app = Flask(__name__)
bcrypt = Bcrypt(app)



login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

principals = Principal(app)
principals._init_app(app)

from project.users.views import users_blueprint
from project.home.views import home_blueprint
from project.home.views import guest_blueprint

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(guest_blueprint)


from models import User

login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
