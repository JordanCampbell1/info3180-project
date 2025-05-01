# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, EmailField, BooleanField, IntegerField, FloatField
from wtforms.validators import InputRequired, DataRequired, Optional
from flask_wtf.file import FileAllowed, FileRequired

class RegisterForm(FlaskForm):
    
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    photo = FileField(
        "Upload Field",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only!"),
        ],
    )
    
class LoginForm(FlaskForm):
    #csrf_token = StringField("csrf_token")  # Explicitly include CSRF token
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class ProfileForm(FlaskForm):
    
    user_id = StringField("UserID", validators=[InputRequired()])
    description = StringField("Description", validators=[Optional()])
    parish = StringField("Parish", validators=[Optional()])
    biography = StringField("Biography", validators=[Optional()])
    sex = StringField("Sex", validators=[Optional()])
    race = StringField("Race", validators=[Optional()])
    birth_year = IntegerField("Birth Year", validators=[Optional()])
    height = FloatField("Height", validators=[Optional()])
    fav_cuisine = StringField("Favourite Cuisine", validators=[Optional()])
    fav_colour = StringField("Favourite Colour", validators=[Optional()])
    fav_school_subject = StringField("Favourite School Subject", validators=[Optional()])
    political = BooleanField("Political", validators=[Optional()])
    religious = BooleanField("Religious", validators=[Optional()])
    family_oriented = BooleanField("Family Oriented", validators=[Optional()])