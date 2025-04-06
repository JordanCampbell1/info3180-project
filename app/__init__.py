from flask import Flask
from .config import Config


from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_wtf import CSRFProtect 


app = Flask(__name__)


app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

csrf = CSRFProtect(app)


# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


from app import views, models