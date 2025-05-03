from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from flask_cors import CORS  # 🔹 Import Flask-CORS

app = Flask(__name__, static_folder="static", static_url_path="/static")

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# # 🔹 Enable CORS - Allow requests from Vue frontend
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

from app import views, models
