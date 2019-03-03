import os.path
from flask import Blueprint, request, jsonify, redirect, url_for, Flask
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flasgger import swag_from, validate
from passlib.hash import pbkdf2_sha256

from .models import Users, UsersSchema, Education, EducationSchema, Role, RoleSchema
from sfi.utils import get_project_root
from sfi.server.errors.errors import InvalidUsage
from .common_functions import post_request_short


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


def user_info(user):
    user_roles = user.roles
    user_role_data = RoleSchema(many=True).dump(user_roles)
    user_data = UsersSchema().dump(user)
    resp =  {
         "user": user_data.data,
         "roles": user_role_data.data
    }
    return jsonify(resp), 200

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
            return user_info(user)
        else:
            raise InvalidUsage('Password incorrect, please try again', status_code=400)
    else:
        raise InvalidUsage('Email incorrect, please try again.', status_code=400)



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
        return user_info(current_user)
    return jsonify({"user": 0}), 200


@bp.route('/register', methods=['POST'])
@swag_from(swagger_auth, methods=['POST'])
def register():
    post_request = request.get_json()
    validate(post_request, 'Researcher', swagger_auth)
    existing = Users.query.filter_by(email=post_request.get('email')).first()

    if not existing:
        mapping = Users.convertToSchema(post_request)
        user_type = Role.query.filter_by(name="researcher").first()
        mapping["roles"] = [user_type]
        return post_request_short(Users, mapping, "Successfully registered")
    else:
        message = 'User with that email already exists'
        raise InvalidUsage(message, status_code=400)

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
        message = "No education information available"
        raise InvalidUsage(message, status_code=404)


