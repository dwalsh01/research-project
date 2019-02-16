import os.path
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flasgger import swag_from, validate
from passlib.hash import pbkdf2_sha256

from .models import Users
from sfi.utils import get_project_root


swagger_auth = os.path.join(get_project_root(), "swagger", "api-auth.yml")
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
        if pbkdf2_sha256.verify(content['password'], user.password):
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
