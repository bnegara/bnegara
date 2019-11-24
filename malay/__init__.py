from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'edeacda59ac156398eb419c6b1ba496a5b8d0250cbf6f09299'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:tokelee@localhost:3306/malay'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Tokelee:141912990abd@Tokelee.mysql.pythonanywhere-services.com/Tokelee$testflask'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
login_manager = LoginManager()

login_manager.init_app(app)
db = SQLAlchemy(app)

login_manager.login_message='Oops Looks like youre not currently logged in'
login_manager.session_protection = 'strong'
login_manager.login_view='users.signin'


#importing blueprints
from malay.main.routes import main
from malay.users.routes import users
from malay.account.routes import accounts
from malay.billing.routes import error

#registering blueprints
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(accounts)
app.register_blueprint(error)

#def create_app(config_class = Config):
    