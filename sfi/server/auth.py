import os.path
from flask import send_from_directory, current_app, render_template, abort, \
     Blueprint, request, jsonify, redirect, url_for, Flask, flash, request, \
     redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flasgger import swag_from, validate
from passlib.hash import pbkdf2_sha256

from .models import Users
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
            return jsonify(user.serialize), 200
        else:
            return '', 400



@bp.route("/api/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("serve"))



@bp.route('/api/user')
def current():
    if current_user.is_authenticated:
        return jsonify({"user": current_user.serialize})
    return jsonify({"user": 0}), 200


@bp.route('/register', methods=['POST'])
@swag_from(swagger_auth, methods=['POST'])
def register():
    post_request = request.get_json()

    validate(post_request, 'Researcher', swagger_auth)
    existing = Users.query.filter_by(email=post_request.get('email')).first()

    if not existing:
        mapping = Users.convertToSchema(post_request)
        new_user = Users(**mapping)
        new_user.saveToDB()

        json_response = {
            'status': 'success',
            'message': 'Successfully registered'
        }
        return jsonify(json_response), 201

    else:
        fail_response = {
            'status': 'failure',
            'message': f'User with that email already exists.'
        }
        return jsonify(fail_response), 202
