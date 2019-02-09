from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from passlib.hash import sha256_crypt

from .models import Users



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
