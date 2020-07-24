import hmac
import os

import flask_sijax
from flask_jwt_extended import JWTManager
from flask import Flask
from flask import session as fsession
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
# from socketio import RedisManager, Server

from app import config

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
os = os


def create_app():
    # init app
    app = Flask(__name__, template_folder='templates')
    api = Api(app)

    # enable debug
    app.debug = True

    # set configuration mode to development
    app.config.from_object(config.DevelopmentConfig)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_BLACKLIST_ENABLED'] = False
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    # init db
    db.init_app(app)
    # needed for pgsql migration script
    migrate = Migrate(app, db)

    @app.before_first_request
    def create_tables():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'pages.login_page'
    login_manager.init_app(app)

    from .model.pgsql import User

    # flask_login recommended to load current user
    @login_manager.user_loader
    def load_user(user_id):
        return User.User.query.get(int(user_id))

    # register blueprints
    # from app.bot.TelegramBot import bot_father as bot_father_blueprint
    # app.register_blueprint(bot_father_blueprint)

    from .auth_ui import auth_ui as auth_ui_blueprint
    app.register_blueprint(auth_ui_blueprint)

    from app.api.auth_api import auth_api as auth_api_blueprint
    app.register_blueprint(auth_api_blueprint)

    from app.api.routes_api import routes_api as routes_api_blueprint
    app.register_blueprint(routes_api_blueprint)

    from .pages_ui import pages_ui as pages_blueprint
    app.register_blueprint(pages_blueprint)

    from app.specific.conversion import conversion as conversion_blueprint
    app.register_blueprint(conversion_blueprint)

    # from app.specific.botadmin import botadmin as botadmin_blueprint
    # app.register_blueprint(botadmin_blueprint)

    # add jwt support on app
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = False
    jwt = JWTManager(app)

    # sijax support
    # The path where you want the extension to create the needed javascript files
    # DON'T put any of your files in this directory, because they'll be deleted!
    app.config["SIJAX_STATIC_PATH"] = basedir + '/static/js/sijax/'

    # You need to point Sijax to the json2.js library if you want to support
    # browsers that don't support JSON natively (like IE <= 7)
    app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

    flask_sijax.Sijax(app)

    # ajax csrf security token
    @app.template_global('csrf_token')
    def csrf_token():
        if "_csrf_token" not in fsession:
            fsession["_csrf_token"] = os.urandom(128)
        return hmac.new(b'config.Config.SECRET_KEY', fsession["_csrf_token"]).hexdigest()

    # init socket io
    # manager = RedisManager('redis://')
    # Server(client_manager=manager)

    return app
