import os.path
from flask import Blueprint, request, jsonify, redirect, url_for, Flask
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flasgger import swag_from, validate
from passlib.hash import pbkdf2_sha256

from .models import CoApplicants, ProposalApplication, ProposalApplicationSchema, Teams,TeamsSchema, \
Users, UsersSchema, Education, EducationSchema, Role, Awards, AwardsSchema, Societies, SocietiesSchema,\
Employment, EmploymentSchema, Funding, FundingSchema, ProposalThemes, ProposalThemesSchema, RoleSchema,\
CoApplicantsSchema, RCTeamMembers, RCTeamMembersSchema, RCTeam, RCTeamSchema

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
    #validate(post_request, 'Researcher', swagger_auth)
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



@bp.route('/profile/education', methods=['POST'])
@login_required
def add_education():
    post_request = request.get_json()
    post_request['user_id'] = current_user.id
    if post_request:
        return post_request_short(Education, post_request, "Education added")

    resp = {
        "status": "failure",
        "message": "No JSON data provided"
    }
    return jsonify(resp), 400

@bp.route('/profile/awards', methods=['GET'])
@login_required
def get_awards():
    user = current_user
    existing = Awards.query.filter_by(user_id=user.id).first()
    if existing:
        awards_schema = AwardsSchema()
        awards = awards_schema.dump(existing)
        return jsonify({"awards": awards.data}), 200
    else:
        return jsonify({"message": "No awards information available"})


@bp.route('/profile/awards', methods=['POST'])
@login_required
def add_awards():
    post_request = request.get_json()
    if post_request:
        return post_request_short(Awards, post_request, "Awards added")

    resp = {
        "status": "failure",
        "message": "No JSON data provided"
    }
    return jsonify(resp), 400

@bp.route('/profile/societies', methods=['GET'])
@login_required
def get_societies():
    user = current_user
    existing = Societies.query.filter_by(user_id=user.id).first()
    if existing:
        societies_schema = SocietiesSchema()
        societies = societies_schema.dump(existing)
        return jsonify({"societies": societies.data}), 200
    else:
        return jsonify({"message": "No societies information available"})

@bp.route('/profile/societies', methods=['POST'])
@login_required
def add_societies():
    post_request = request.get_json()
    if post_request:
        return post_request_short(Societies, post_request, "Societies added")

    resp = {
        "status": "failure",
        "message": "No JSON data provided"
    }
    return jsonify(resp), 400

@bp.route('/profile/employment', methods=['GET'])
@login_required
def get_employment():
    user = current_user
    existing = Employment.query.filter_by(user_id=user.id).first()
    if existing:
        employment_schema = EmploymentSchema()
        employment = employment_schema.dump(existing)
        return jsonify({"employment": employment.data}), 200
    else:
        return jsonify({"message": "No employment information available"})

@bp.route('/profile/employment', methods=['POST'])
@login_required
def add_employment():
    post_request = request.get_json()
    if post_request:
        return post_request_short(Employment, post_request, "Employment added")

    resp = {
        "status": "failure",
        "message": "No JSON data provided"
    }
    return jsonify(resp), 400

@bp.route('/profile/funding', methods=['GET'])
@login_required
def get_funding():
    user = current_user
    existing = Funding.query.filter_by(user_id=user.id).first()
    if existing:
        funding_schema = FundingSchema()
        funding = funding_schema.dump(existing)
        return jsonify({"funding": funding.data}), 200
    else:
        return jsonify({"message": "No funding information available"})

@bp.route('/profile/funding', methods=['POST'])
@login_required
def add_funding():
    post_request = request.get_json()
    if post_request:
        return post_request_short(Funding, post_request, "Funding added")

    resp = {
        "status": "failure",
        "message": "No JSON data provided"
    }
    return jsonify(resp), 400

@bp.route('/profile/team', methods=['GET'])
@login_required
def get_team():
    user = current_user
    existing = Teams.query.filter_by(person_id=user.id).first()
    if existing:
        teams_schema = TeamsSchema()
        teams = teams_schema.dump(existing)
        return jsonify({"teams": teams.data}), 200
    else:
        return jsonify({"message": "No teams information available"})

@bp.route('/profile/team', methods=['POST'])
@login_required
def add_team():
    post_request = request.get_json()
    if post_request:
        return post_request_short(Teams, post_request, "Teams added")

    resp = {
        "status": "failure",
        "message": "No JSON data provided"
    }
    return jsonify(resp), 400






@bp.route('/api/user/application', methods=['GET'])
@login_required
def get_application():
    user = current_user
    existing = ProposalApplication.query.filter_by(applicant=user.id).first()
    if existing:
        proposal_application_schema = ProposalApplicationSchema()
        proposal_application = proposal_application_schema.dump(existing)
        return jsonify({"proposal_application": proposal_application.data}), 200
    else:
        raise InvalidUsage("No applications available for this user", status_code=404)


@bp.route('/proposal_themes', methods=['GET'])
@login_required
def get_proposal_themes():
    user = current_user
    existing = ProposalThemes.query.all()
    if existing:
        proposal_themes_schema = ProposalThemesSchema()
        proposal_themes = proposal_themes_schema.dump(existing)
        return jsonify({"proposal_themes": proposal_themes.data}), 200
    else:
        return jsonify({"message": "No Proposal Themes information available"})

@bp.route('/proposal_themes', methods=['POST'])
@login_required
def add_proposal_themes():
    post_request = request.get_json()
    if post_request:
        return post_request_short(ProposalThemes, post_request, "Application added")

    resp = {
        "status": "failure",
        "message": "No JSON data provided"
    }
    return jsonify(resp), 400


@bp.route('/rc_team', methods=['GET'])
@login_required
def get_rc_team():
    '''
    Search RCTeamMembers for team_member = current_user.id
    from that, you get the team_id

    query RCTeam teamid = teamid
    '''
    user = current_user
    lst = []
    members = RCTeamMembers.query.filter_by(team_member=user.id).all()
    for member in members:
        lst.append(member.team_id)
    existing = [RCTeam.query.filter_by(team_id=ident).one() for ident in lst]
    if existing:
        rc_team_schema = RCTeamSchema(many=True)
        rc_team = rc_team_schema.dump(existing)
        return jsonify({"rc_team": rc_team.data}), 200
    else:
        raise InvalidUsage("No RC Team information available", status_code=404)

@bp.route('/rc_team_members', methods=['GET'])
@login_required
def get_rc_team_members():
    user = current_user
    existing = RCTeamMembers.query.filter_by(team_member=user.id).all()
    if existing:
        rc_team_members_schema = RCTeamMembersSchema(many=True)
        rc_team_members = rc_team_members_schema.dump(existing)
        return jsonify({"rc_team": rc_team_members.data}), 200
    else:
        raise InvalidUsage("No RC Team Members information available", status_code=404)