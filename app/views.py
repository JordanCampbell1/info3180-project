"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file

# from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Profile, Favourite
from sqlalchemy import func
import os
from app import app, db, csrf
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
    send_from_directory,
    jsonify,
)
from werkzeug.utils import secure_filename
from app.models import User, Profile, Favourite
from app.forms import LoginForm, ProfileForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

from flask_wtf.csrf import generate_csrf

from functools import wraps
from datetime import datetime, timedelta, timezone
import jwt
from sqlalchemy.exc import SQLAlchemyError

##Helper Function

blacklisted_tokens = set()


def create_token(user_id):  # jwt token
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=6),
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):  # jwt token
    return jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])


def jwt_required(f):  ##jwt required decorator to attach to the relevant routes
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Missing token"}), 401

        try:
            token = auth_header.split(" ")[1]  # "Bearer <token>"

            # Check if the token is blacklisted
            if token in blacklisted_tokens:
                return (
                    jsonify(
                        {"message": "Token has been blacklisted. Please log in again."}
                    ),
                    401,
                )

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


@app.route("/")
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

            user = User(username, password, name, email, filename)

            db.session.add(user)
            db.session.commit()

            return (
                jsonify(
                    {
                        "message": "User registered successfully",
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "name": user.name,
                            "email": user.email,
                            "photo": filename,
                        },
                    }
                ),
                201,
            )

        except SQLAlchemyError as e:
            db.session.rollback()
            return (
                jsonify(
                    {
                        "message": "Something went wrong while saving to the database.",
                        "error": str(e.__dict__.get("orig")),
                    }
                ),
                500,
            )

    # Handle form validation failure
    return (
        jsonify(
            {
                "errors": form.errors,
                "message": "User registration failed due to validation errors.",
            }
        ),
        400,
    )


@app.route(
    "/api/csrf-token", methods=["GET"]
)  # need to be called first and attached to the header as "X-CSRFToken" : <csrf_token> before each form request to the API
def get_csrf():
    return jsonify({"csrf_token": generate_csrf()})


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

            return (
                jsonify(
                    {
                        "message": "Login successful",
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            # include other safe fields if needed
                        },
                        "token": token,
                    }
                ),
                200,
            )
        else:
            return jsonify({"message": "Invalid username or password"}), 401

    # Handle form validation failure
    return (
        jsonify(
            {
                "errors": form.errors,
                "message": "User login failed due to validation errors.",
            }
        ),
        400,
    )


@csrf.exempt  # need to do when jwt is used for the route
@app.route("/api/auth/logout", methods=["POST"])
@jwt_required  # once jwtrequired decorator is used, user_id will be passed to the view function
def logout(user_id):
    # Get the token from the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"message": "Missing token"}), 401

    token = auth_header.split(" ")[1]  # "Bearer <token>"

    # Add the token to the blacklist
    blacklisted_tokens.add(token)

    return jsonify({"message": f"Logout successful for User {user_id}"}), 200


@app.route("/api/profiles", methods=["GET"])
@csrf.exempt
@jwt_required
def get_all_profiles(user_id):

    # 1. Join Profile and User, order by User.date_joined DESC
    results = (
        db.session.query(Profile, User)
        .join(User, Profile.user_id_fk == User.id)
        .order_by(Profile.created_at.desc())
        .all()
    )

    # 2. Combine data from both models
    profiles_with_user_info = []
    for profile, user in results:
        profiles_with_user_info.append(
            {
                "id": profile.id,
                "user_id": user.id,
                "description": profile.description,
                "parish": profile.parish,
                "biography": profile.biography,
                "sex": profile.sex,
                "race": profile.race,
                "birth_year": profile.birth_year,
                "height": profile.height,
                "fav_cuisine": profile.fav_cuisine,
                "fav_colour": profile.fav_colour,
                "fav_school_sibject": profile.fav_school_subject,
                "political": profile.political,
                "religious": profile.religious,
                "family_oriented": profile.family_oriented,
                # From User
                "username": user.username,
                "photo": user.photo,
                "date_joined": user.date_joined.isoformat(),
                "profile_created": profile.created_at.isoformat(),
            }
        )

    return jsonify(profiles_with_user_info), 200


@app.route("/api/profiles", methods=["POST"])
def create_profile():

    form = ProfileForm()

    if form.validate_on_submit:

        user_id = form.user_id.data

        # Check if user already has 3 profiles
        profile_count = Profile.query.filter_by(user_id_fk=user_id).count()
        if profile_count >= 3:
            return jsonify({"message": "You can only create up to 3 profiles."}), 400

        description = form.description.data
        parish = form.parish.data
        biography = form.biography.data
        sex = form.sex.data
        race = form.race.data
        birth_year = form.birth_year.data
        height = form.height.data
        fav_cuisine = form.fav_cuisine.data
        fav_colour = form.fav_colour.data
        fav_school_subject = form.fav_school_subject.data
        political = form.political.data
        religious = form.religious.data
        family_oriented = form.family_oriented.data

        profile = Profile(
            user_id,
            description,
            parish,
            biography,
            sex,
            race,
            birth_year,
            height,
            fav_cuisine,
            fav_colour,
            fav_school_subject,
            political,
            religious,
            family_oriented,
        )

        db.session.add(profile)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Profile created successfully",
                    "profile": profile.to_dict(),
                }
            ),
            201,
        )

    # Handle form validation failure
    return (
        jsonify(
            {
                "errors": form.errors,
                "message": "User login failed due to validation errors.",
            }
        ),
        400,
    )


# Dominic


# Get details of a specific profile
##########################################################################
# Working in Postman#######################################################
##########################################################################
@app.route("/api/profiles/<int:profile_id>", methods=["GET"])
@csrf.exempt
@jwt_required
def get_profile(user_id, profile_id):
    print("get_profile route was reached")
    result = (
        db.session.query(Profile, User)
        .join(User, Profile.user_id_fk == User.id)
        .filter(Profile.id == profile_id)
        .first()
    )

    if not result:
        return jsonify({"message": "Profile not found."}), 404

    profile, user = result

    profile_data = {
        "id": profile.id,
        "user_id": user.id,
        "description": profile.description,
        "parish": profile.parish,
        "biography": profile.biography,
        "sex": profile.sex,
        "race": profile.race,
        "birth_year": profile.birth_year,
        "height": profile.height,
        "fav_cuisine": profile.fav_cuisine,
        "fav_colour": profile.fav_colour,
        "fav_school_sibject": profile.fav_school_subject,
        "political": profile.political,
        "religious": profile.religious,
        "family_oriented": profile.family_oriented,
        "username": user.username,
        "photo": user.photo,
        "date_joined": user.date_joined.isoformat(),
        "profile_created": profile.created_at.isoformat(),
    }

    return jsonify(profile_data), 200


# Add user to favourites
##########################################################################
# Working in Postman#######################################################
##########################################################################
@app.route("/api/profiles/<int:user_id2>/favourite", methods=["POST"])
@csrf.exempt
@jwt_required
def favourite_user(user_id, user_id2):
    current_user_id = user_id
    if current_user_id == user_id2:
        return jsonify({"error": "You can't favourite yourself."}), 400

    already_fav = Favourite.query.filter_by(
        user_id_fk=current_user_id, fav_user_id_fk=user_id2
    ).first()
    if already_fav:
        return jsonify({"message": "User is already in favourites."}), 200

    fav = Favourite(user_id_fk=current_user_id, fav_user_id_fk=user_id2)
    db.session.add(fav)
    db.session.commit()
    return jsonify({"message": "User added to favourites"}), 201


# extra
#################################################################
# Working in Postman#######################################################
# UPDATE PROFILE
#################################################################
@app.route("/api/profiles/<int:profile_id>", methods=["PUT"])
@csrf.exempt
@jwt_required
def update_profile(user_id, profile_id):
    profile = db.session.get(Profile, profile_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    data = request.get_json()

    for field in [
        "description",
        "parish",
        "biography",
        "sex",
        "race",
        "birth_year",
        "height",
        "fav_cuisine",
        "fav_colour",
        "fav_school_subject",
        "political",
        "religious",
        "family_oriented",
    ]:
        if field in data:
            setattr(profile, field, data[field])

    db.session.commit()
    return jsonify({"message": "Profile updated", "profile": profile.to_dict()}), 200


#################################################################

# Get all profiles that match a specific profile's criteria
# Part 2 point 7


#################################################################
# Working in Postman#######################################################
#################################################################
@app.route("/api/profiles/matches/<int:profile_id>", methods=["GET"])
@csrf.exempt
@jwt_required
def match_profiles(user_id, profile_id):
    # print("this is user id", user_id)
    # print("this is profile id", profile_id)
    current = Profile.query.filter_by(id=profile_id, user_id_fk=user_id).first()

    # print("this is current profile", current)

    if not current:
        return jsonify({"error": "Profile not found"}), 404

    matches = []
    all_profiles = Profile.query.filter(
        Profile.id != profile_id, Profile.user_id_fk != user_id
    ).all()

    # print("this is all profiles", all_profiles)

    match_fields = [
        "fav_cuisine",
        "fav_colour",
        "fav_school_subject",
        "political",
        "religious",
        "family_oriented",
    ]

    for profile in all_profiles:
        if not profile.birth_year or not current.birth_year:
            continue

        if abs(profile.birth_year - current.birth_year) > 5:
            continue

        if not profile.height or not current.height:
            continue

        height_diff_in_inches = abs(profile.height - current.height) * 39.37

        # print("height diff in inches", 3 <= int(height_diff_in_inches) <= 10)

        if not (3 <= int(height_diff_in_inches) <= 10):
            continue

        # print("this is profile in the validation logic", profile)

        matched_fields = [
            field
            for field in match_fields
            if getattr(profile, field) == getattr(current, field)
        ]

        if len(matched_fields) >= 3:
            profile_dict = profile.to_dict()
            profile_dict["matched_fields"] = matched_fields
            matches.append(profile_dict)

    return jsonify(matches), 200


# Search profiles
#################################################################
# Working in Postman#######################################################
#################################################################


@app.route("/api/search", methods=["GET"])
@csrf.exempt
@jwt_required
def search_profiles(user_id):
    name = request.args.get("name")
    birth_year = request.args.get("birth_year")
    sex = request.args.get("sex")
    race = request.args.get("race")

    # Start query with Profile + User join
    query = (
        db.session.query(Profile, User)
        .join(User, Profile.user_id_fk == User.id)
        .filter(User.id != user_id)  # Exclude current user's profiles
    )

    # Apply filters conditionally
    if name:
        query = query.filter(func.lower(User.username).like(f"%{name.lower()}%"))
    if birth_year:
        query = query.filter(Profile.birth_year == int(birth_year))
    if sex:
        query = query.filter(func.lower(Profile.sex) == sex.lower())
    if race:
        query = query.filter(func.lower(Profile.race) == race.lower())

    # Execute and format response
    results = query.order_by(Profile.created_at.desc()).all()

    profiles_with_user_info = []
    for profile, user in results:
        profiles_with_user_info.append(
            {
                "id": profile.id,
                "user_id": user.id,
                "description": profile.description,
                "parish": profile.parish,
                "biography": profile.biography,
                "sex": profile.sex,
                "race": profile.race,
                "birth_year": profile.birth_year,
                "height": profile.height,
                "fav_cuisine": profile.fav_cuisine,
                "fav_colour": profile.fav_colour,
                "fav_school_sibject": profile.fav_school_subject,
                "political": profile.political,
                "religious": profile.religious,
                "family_oriented": profile.family_oriented,
                "username": user.username,
                "photo": user.photo,
                "date_joined": user.date_joined.isoformat(),
                "profile_created": profile.created_at.isoformat(),
            }
        )

    return jsonify(profiles_with_user_info), 200


# Testcase
# http://localhost:8080/api/search?birth_year=2002&race=Black&sex=Female
# return id=3


# Get details of a user
#################################################################
# Working in Postman#######################################################
#################################################################
@app.route("/api/users/<int:user_id2>", methods=["GET"])
@csrf.exempt
@jwt_required
def get_user(user_id, user_id2):
    user = db.session.get(User, user_id2)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404


# Get users that a user has favourited


##########################################################################
# Working in Postman#######################################################
##########################################################################
@app.route("/api/users/<int:user_id2>/favourites", methods=["GET"])
@csrf.exempt
@jwt_required
def user_favourites(user_id, user_id2):
    favs = Favourite.query.filter_by(user_id_fk=user_id2).all()
    data = []
    for fav in favs:
        user = db.session.get(User, fav.fav_user_id_fk)
        if user:
            data.append(user.to_dict())
    return jsonify(data), 200


##########################################################################
# Working in Postman#######################################################
##########################################################################
@app.route("/api/users/favourites/<int:N>", methods=["GET"])
@csrf.exempt
@jwt_required
def top_favourited_users(user_id, N):
    counts = (
        db.session.query(
            Favourite.fav_user_id_fk,
            func.count(Favourite.fav_user_id_fk).label("count"),
        )
        .group_by(Favourite.fav_user_id_fk)
        .order_by(func.count(Favourite.fav_user_id_fk).desc())
        .limit(N)
        .all()
    )
    result = []
    for user_id, count in counts:
        user = db.session.get(User, user_id)
        if user:
            udata = user.to_dict()
            udata["favourite_count"] = count
            result.append(udata)
    return jsonify(result), 200


###
# The functions below should be applicable to all Flask apps.


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = "Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error,
            )
            error_messages.append(message)

    return error_messages


@app.route("/<file_name>.txt")
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + ".txt"
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers["X-UA-Compatible"] = "IE=Edge,chrome=1"
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template("404.html"), 404
