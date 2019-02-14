import os.path
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flasgger import swag_from
from passlib.hash import sha256_crypt

from .models import Users
from sfi.utils import get_project_root

swagger_dir = os.path.join(get_project_root(), "swagger")

bp = Blueprint('auth', __name__)

login_manager = LoginManager()



@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)


@bp.route('/login_user' , methods=['POST'])
def login():
    content = request.get_json()
    user = Users.query.filter_by(email=content['email']).first()
    if user:
        if sha256_crypt.verify(content['password'], user.password):
            login_user(user, remember=True)
            return jsonify(user.serialize), 200
        else:
            return '', 400



@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("serve"))



@bp.route('/current')
def current():
    if current_user.is_authenticated:
        return jsonify(current_user.serialize)
    return jsonify({"user": "False"}), 200


@bp.route('/register', methods=['POST'])
@swag_from(f'{swagger_dir}/register.yml', methods=['POST'])
def register():
    post_request = request.get_json()

    existing = Users.query.filter_by(email=post_request.get('email')).first()
    if not existing:
        new_user = Users(
            post_request.get('first_name'),
            post_request.get('second_name'),
            post_request.get('job_title'),
            post_request.get('prefix'),
            post_request.get('suffix'),
            post_request.get('phone'),
            post_request.get('phone_extension'),
            post_request.get('email'),
            post_request.get('password'),
            post_request.get('orcid')
        )

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
        return jsonify({'dontcomplain': 'thanks'}), 200


