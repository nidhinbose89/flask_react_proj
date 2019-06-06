import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_restful import Api


# config
app = Flask(__name__)
cors = CORS(app)
app.config.from_object(os.environ['APP_SETTINGS'])

# extensions
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

api = Api(app, prefix='/api')

from digital_lotus.views import (ResourceViews, LoginViews, LogoutViews, RegisterViews)  # noqa

api.add_resource(ResourceViews,
                 '/user',
                 '/user/<int:user_id>'
                 )
api.add_resource(LoginViews,
                 '/login'
                 )
api.add_resource(LogoutViews,
                 '/logout'
                 )

api.add_resource(RegisterViews,
                 '/register'
                 )
