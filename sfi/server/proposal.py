import os
from flask import Blueprint, jsonify, request
from flasgger import swag_from, validate
from sfi.utils import get_project_root
from flask_login import current_user, login_required
from .models import ProposalCall, LongProposalSchema, ShortProposalSchema, \
    ApplicationDraft, ApplicationDraftSchema, ProposalApplication, Users, \
    CoApplicants, ApplicationCollaborators, PendingReviews,ProposalApplicationSchema

from .common_functions import post_request_short, attempt_insert
from sfi.server.errors.errors import InvalidUsage

from sqlalchemy.sql import func
import datetime

swagger_prop = os.path.join(get_project_root(), "swagger", "api-proposal.yml")
bp = Blueprint('proposal', __name__, url_prefix="/calls")

@bp.route('/list')
@swag_from(swagger_prop, methods=['GET'])
def list_proposals():
    proposals = ProposalCall.query.all()
    schema = ShortProposalSchema(many=True)
    return schema.jsonify(proposals), 200


@bp.route('/show/<int:call_id>')
def show_proposal(call_id):
    proposal = ProposalCall.query.filter_by(id=call_id).first()
    schema = LongProposalSchema()
    if proposal is None:
        return '', 404
    return schema.jsonify(proposal), 200


@bp.route('/add', methods=['POST'])
def add_proposal():
    post_request = request.get_json()
    if post_request:
        post_request["amount_left"] = 0
        return post_request_short(ProposalCall, post_request, "Proposal Call Added")

    message = "No JSON data provided"
    raise InvalidUsage(message, status_code=400)


@bp.route('/apply/<int:call_id>/draft', methods=['POST'])
def save_draft(call_id):
    '''
    Draft =>;
    prop_id
    applicant-id
    JSON
    '''
    json = request.get_json()
    if json and current_user.is_authenticated:
        applicant_id = current_user.id
        data = {
            "prop_id": call_id,
            "applicant": applicant_id,
            "draft": json
        }
        existing_draft = ApplicationDraft.query.filter_by(prop_id=call_id, applicant=applicant_id).first()
        if existing_draft:
            existing_draft.draft = json
            existing_draft.saveToDB()
            return jsonify({'message': 'Successfully updated existing draft!'}), 200
        else:
            return post_request_short(ApplicationDraft, data, "Saved draft")

    resp = {
        "status": "failure",
        "message": "Please log-in or provide valid JSON"
    }
    return jsonify(resp), 400


@bp.route('/apply/<int:call_id>/draft', methods=['GET'])
def get_draft(call_id):
    if current_user.is_authenticated:
        applicant_id = current_user.id
        draft = ApplicationDraft.query.filter_by(prop_id=call_id, applicant=applicant_id).first()
        if draft:
            data = ApplicationDraftSchema().dump(draft).data
            data['applicant'] = applicant_id
            data['prop_id'] = call_id
            return jsonify(data), 200
        else:
            return jsonify({}), 404
    resp = {
        "status": "failure",
        "message": "Please log-in"
    }
    return jsonify(resp), 400

@bp.route('/apply/draft/all', methods=['GET'])
def get_all():
    if current_user.is_authenticated:
        applicant_id = current_user.id
        draft = ApplicationDraft.query.filter_by(applicant=applicant_id).all()
        if draft:
            data = ApplicationDraftSchema(many=True).dump(draft)
            return jsonify(data.data), 200
        else:
            return jsonify({"message": "no drafts found"}), 200
    resp = {
        "status": "failure",
        "message": "Please log-in"
    }
    return jsonify(resp), 400


def parse_co_applicants(co_apps, application):
    for co_app_dict in co_apps:
        co_app_email = co_app_dict.get('email')
        user = Users.query.filter_by(email=co_app_email).first()
        if user is None:
            raise InvalidUsage("co-applicant email doesn't exist")
        d = {
            "co_user": user.id,
            "propapp": application
        }
        attempt_insert(CoApplicants, d)

def parse_collaborators(collabs, application):
    for collab_info in collabs:
        email = collab_info.get('email')
        user = Users.query.filter_by(email=email).first()
        if user is None:
            raise InvalidUsage("collaborator(s) email doesn't exist")
        d = {
            **collab_info,
            "propapp": application
        }
        attempt_insert(ApplicationCollaborators, d)

def assign_app_reviewers(app):
    deadline = datetime.date.today() + datetime.timedelta(weeks=12)
    reviewers = Users.query.filter(Users.roles.any(name="reviewer")).order_by(func.random()).all()
    num_allocate = 2 if len(reviewers) > 1 else 1
    for num in range(num_allocate):
        reviewer = reviewers[num]
        data = {
            "reviewer_id": reviewer.id,
            "app_id": app.id,
            "deadline": deadline
        }
        attempt_insert(PendingReviews, data)


@bp.route('/apply/get/<int:call_id>', methods=['GET'])
@login_required
def get_application(call_id):
    print(call_id)
    existing = ProposalApplication.query.filter_by(id=call_id).first()
    if existing:
        print('exists')
        data = ProposalApplicationSchema().dump(existing)
        return jsonify(data.data), 200
    else:
        return jsonify({"message": "no proposal found"}), 200
    resp = {
        "status": "failure",
        "message": "Please log-in"
    }
    return jsonify(resp), 400



@bp.route('/apply/<int:call_id>', methods=['POST'])
@login_required
def apply(call_id):
    post_request = request.get_json()
    if post_request:
        uid = current_user.id
        existing = ProposalApplication.query.filter_by(applicant=uid, proposal_id=call_id).first()
        if existing:
            raise InvalidUsage("Application already submitted, awaiting reviewing.")

        co_apps = post_request.get("list_of_co_applicants")
        collabs = post_request.get("list_of_collaborators")
        post_request['applicant'] = current_user.id
        post_request["list_of_co_applicants"] = []
        post_request["list_of_collaborators"] = []
        post_request["applicant"] = uid
        post_request["proposal_id"] = call_id
        app = attempt_insert(ProposalApplication, post_request)
        parse_co_applicants(co_apps, app)
        parse_collaborators(collabs, app)
        assign_app_reviewers(app)
        resp = {
            "message": "Application submitted"
        }
        return jsonify(resp), 201
    raise InvalidUsage("No JSON data provided")

@bp.route('/application/<int:app-id>/accept')
def accept_app(app_id):
    pass

