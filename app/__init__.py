from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from flask_cors import CORS  # 🔹 Import Flask-CORS

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)


flask_env = app.config["FLASK_ENV"]

if flask_env == "development":
    # # 🔹 Enable CORS - Allow requests from Vue frontend
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
else:
    # Restrict or disable CORS in production
    CORS(app, origins=["https://jam-date.onrender.com"], supports_credentials=True)

# # 🔹 Set up the upload folder for images (dynamically)
import os

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


from app import views, models
