"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
from app import app, db
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
    send_from_directory,
    jsonify
)
from werkzeug.utils import secure_filename
from app.models import User, Profile, Favourite
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

from flask_wtf.csrf import generate_csrf 

from functools import wraps
from datetime import datetime, timedelta, timezone
import jwt
from sqlalchemy.exc import SQLAlchemyError

##Helper Function

def create_token(user_id): #jwt token
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=2)
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

def decode_token(token): #jwt token
    return jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])

def jwt_required(f): ##jwt required decorator to attach to the relevant routes
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Missing token"}), 401

        try:
            token = auth_header.split(" ")[1]  # "Bearer <token>"
            data = decode_token(token)
            user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except Exception as e:
            return jsonify({"message": "Invalid token"}), 401

        return f(user_id, *args, **kwargs)
    return wrapper



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route("/api/register", methods=["POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        
        
        try: 
            username = form.username.data
            password = form.password.data
            name = form.name.data
            email = form.email.data
            
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))     
            
            user = User(username,password,name,email,filename)
            
            db.session.add(user)
            db.session.commit()
            
            return jsonify({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "name": user.name,
                    "email": user.email,
                    "photo": filename
                }
            }), 201
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({
                "message": "Something went wrong while saving to the database.",
                "error": str(e.__dict__.get("orig"))
            }), 500
    
    # Handle form validation failure
    return jsonify({
        "errors": form.errors,
        "message": "User registration failed due to validation errors."
    }), 400
        
        

    

@app.route('/api/csrf-token', methods=['GET']) #need to be called first and attached to the header as "X-CSRFToken" : <csrf_token> before each form request to the API
def get_csrf(): 
    return jsonify({'csrf_token': generate_csrf()})  
    
@app.route("/uploads/<filename>", methods=["GET"])
def get_image(filename):
    upload_folder = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"])

    # print("this is uplaod folder", upload_folder)
    # print("get image route was reached")

    return send_from_directory(upload_folder, filename)


@app.route("/api/auth/login", methods=["POST"])
def login():
    form = LoginForm()

    # change this to actually validate the entire form submission
    # and not just one field
    if form.validate_on_submit():
        # Get the username and password values from the form.

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):

            # Using your model, query database for a user based on the username
            # and password submitted. Remember you need to compare the password hash.
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.
            
            token = create_token(user.id)
            
            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    # include other safe fields if needed
                },
                "token": token
            }), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
        
    # Handle form validation failure
    return jsonify({
        "errors": form.errors,
        "message": "User login failed due to validation errors."
    }), 400


###
# The functions below should be applicable to all Flask apps.



# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404