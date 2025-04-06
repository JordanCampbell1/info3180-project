# Add any model classes for Flask-SQLAlchemy here

from . import db
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import func


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    photo = db.Column(db.String(80))
    date_joined = db.Column(db.DateTime, default=func.now())


    def __init__(self, username, password, name=None, email=None, photo=None):
        self.username = username
        self.password = generate_password_hash(password, method="pbkdf2:sha256")
        self.name = name
        self.email = email
        self.photo = photo

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # python 3 support

    def __repr__(self):
        return "<User %r>" % (self.username)
    

from . import db

class Profile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # Foreign key to User model
    description = db.Column(db.String(200), nullable=True)
    parish = db.Column(db.String(20), nullable=True)
    biography = db.Column(db.String(200), nullable=True)
    sex = db.Column(db.String(10), nullable=True)
    race = db.Column(db.String(10), nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Float, nullable=True)
    fav_cuisine = db.Column(db.String(30), nullable=True)
    fav_colour = db.Column(db.String(15), nullable=True)
    fav_school_subject = db.Column(db.String(20), nullable=True)
    political = db.Column(db.Boolean, nullable=True)
    religious = db.Column(db.Boolean, nullable=True)
    family_oriented = db.Column(db.Boolean, nullable=True)
    
    user = db.relationship("User", foreign_keys=[user_id_fk])

    def __init__(
        self, user_id_fk, description=None, parish=None, biography=None, sex=None, race=None, 
        birth_year=None, height=None, fav_cuisine=None, fav_colour=None, fav_school_subject=None, 
        political=None, religious=None, family_oriented=None
    ):
        self.user_id_fk = user_id_fk
        self.description = description
        self.parish = parish
        self.biography = biography
        self.sex = sex
        self.race = race
        self.birth_year = birth_year
        self.height = height
        self.fav_cuisine = fav_cuisine
        self.fav_colour = fav_colour
        self.fav_school_subject = fav_school_subject
        self.political = political
        self.religious = religious
        self.family_oriented = family_oriented

    def __repr__(self):
        return f"<Profile of User {self.user_id_fk}>"

class Favourite(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", foreign_keys=[user_id_fk])
    favourite_user = db.relationship("User", foreign_keys=[fav_user_id_fk])

    def __repr__(self):
        return f"<Favourite {self.user_id_fk} -> {self.fav_user_id_fk}>"