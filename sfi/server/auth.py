import os.path
from flask import send_from_directory, current_app, render_template, abort, \
     Blueprint, request, jsonify, redirect, url_for, Flask, flash, request, \
     redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flasgger import swag_from, validate
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from .models import Users, UsersSchema
from sfi.utils import get_project_root

import os
from werkzeug.utils import secure_filename



swagger_auth = os.path.join(get_project_root(), "swagger", "api-auth.yml")
bp = Blueprint('auth', __name__)
login_manager = LoginManager()


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
            return jsonify({"error": "invalid password" }), 400
    else:
        return jsonify({"error": "email does not exist"}), 400



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
        try:
            new_user = Users(**mapping)
            new_user.saveToDB()

            json_response = {
                'status': 'success',
                'message': 'Successfully registered'
            }
            return jsonify(json_response), 201

        except IntegrityError as e:
            short_error = e.orig.diag.message_primary
            invalid_format = {
                'status': 'failure',
                'message': 'invalid_format',
                'error': short_error
            }
            return jsonify(invalid_format), 400
    else:
        fail_response = {
            'status': 'failure',
            'message': 'User with that email already exists'
        }
        return jsonify(fail_response), 400



@bp.route('/profile/education', methods=['POST'])
def add_education():
    post_request = request.get_json()

@bp.route('/profile/education', methods=['GET'])
def get_education():
    pass

