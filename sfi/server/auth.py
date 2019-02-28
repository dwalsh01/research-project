import os.path
from flask import send_from_directory, current_app, render_template, abort, \
     Blueprint, request, jsonify, redirect, url_for, Flask, flash, request, \
     redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flasgger import swag_from, validate
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from .models import Users, UsersSchema, Education, EducationSchema, UserTypes
from sfi.utils import get_project_root
from .common_functions import post_request_short

import os
from werkzeug.utils import secure_filename



swagger_auth = os.path.join(get_project_root(), "swagger", "api-auth.yml")
bp = Blueprint('auth', __name__)
login_manager = LoginManager()

sampleTeams = [
    {
        "id": 1,
        "person_id": 6,
        "start_date": "01/01/2019",
        "end_date": "01/02/2019",
        "name": "The A Team",
        "position": "Administrator",
        "primary_attribution": 1
    },
    {
        "id": 1,
        "person_id": 6,
        "start_date": "01/01/2019",
        "end_date": "01/03/2019",
        "name": "The B Team",
        "position": "Administrator",
        "primary_attribution": 2
    },
    {
        "id": 1,
        "person_id": 6,
        "start_date": "03/01/2019",
        "end_date": "05/02/2019",
        "name": "The C Team",
        "position": "Researcher",
        "primary_attribution": 3
    },
    {
        "id": 1,
        "person_id": 6,
        "start_date": "02/03/2019",
        "end_date": "05/05/2019",
        "name": "The D Team",
        "position": "Researcher",
        "primary_attribution": 5
    }
]
# THIS WILL NEED TO BE MOVED I THINK THIS WILL
# HANDLE THE VARIOUS ERROR RESPONSE TO FRONT END (HOPEFULLY)
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@bp.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# END OF WHAT NEEDS TO BE MOVED

ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('auth.upload_file', filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)

@bp.route('/login_user' , methods=['POST'])
def login():
    content = request.get_json()
    if current_user.is_authenticated:
        return redirect(url_for("serve"))
    user = Users.query.filter_by(email=content['email']).first()
    if user:
        if pbkdf2_sha256.verify(content['password'], user.password):
            login_user(user, remember=True)
            user_schema = UsersSchema()
            return user_schema.jsonify(user), 200
        else:
            raise InvalidUsage(message='Password incorrect, please try again', status_code=400)
    else:
        raise InvalidUsage(message='Email incorrect, please try again.', status_code=400)



@bp.route("/api/logout")
@login_required
def logout():
    logout_user()
    # keep this here for testing, comment it out and use bottom
    # return statement with production build
    return jsonify({"logout": "success"}), 200
    # return redirect(url_for("serve"))



@bp.route('/api/user')
def current():
    if current_user.is_authenticated:
        user_schema = UsersSchema()
        user = user_schema.dump(current_user)
        return jsonify({"user": user.data  }), 200
    return jsonify({"user": 0}), 200


@bp.route('/register', methods=['POST'])
@swag_from(swagger_auth, methods=['POST'])
def register():
    post_request = request.get_json()
    validate(post_request, 'Researcher', swagger_auth)
    existing = Users.query.filter_by(email=post_request.get('email')).first()

    if not existing:
        mapping = Users.convertToSchema(post_request)
        user_type = UserTypes.query.filter_by(user_name="researcher").first()
        mapping["user_type"] = user_type.user_id
        return post_request_short(Users, mapping, "Successfully registered")
    else:
        fail_response = {
            'status': 'failure',
            'message': 'User with that email already exists'
        }
        return jsonify(fail_response), 400



'''
Profiles
&&
Related Information
'''
@bp.route('/api/get_teams', methods=['GET'])
@login_required
def get_teams():
    return jsonify({"teams": sampleTeams }), 200


# @bp.route('/profile/education', methods=['POST'])
# def add_education():
#     post_request = request.get_json()


@bp.route('/profile/education', methods=['GET'])
@login_required
def get_education():
    user = current_user
    existing = Education.query.filter_by(user_id=user.id).first()
    if existing:
        edu_schema = EducationSchema()
        edu = edu_schema.dump(existing)
        return jsonify({"education": edu.data}), 200
    else:
        return jsonify({"message": "No education information available"})


