# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, EmailField
from wtforms.validators import InputRequired, DataRequired
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
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
