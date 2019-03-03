import os
from flask import Blueprint, jsonify, request
from flasgger import swag_from, validate
from sfi.utils import get_project_root
from flask_login import current_user
from .models import ProposalCall, LongProposalSchema, ShortProposalSchema, \
    ApplicationDraft, ApplicationDraftSchema

from .common_functions import post_request_short


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
        post_request["amount_left"] = post_request.get('award_amount', 0)
        return post_request_short(ProposalCall, post_request, "Proposal call added")

    resp = {
        "status": "failure",
        "message": "No JSON data provided"
    }
    return jsonify(resp), 400


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
            return jsonify({}), 404
    resp = {
        "status": "failure",
        "message": "Please log-in"
    }
    return jsonify(resp), 400

@bp.route('/apply/<int:call_id>', methods=['POST'])
def apply(call_id):
    post_request = request.get_json()
    if post_request:
        return post_request_short(ProposalApplication, post_request, "Application Submitted")

    resp = {
        "status": "failure",
        "message": "No JSON data provided"
    }
    return jsonify(resp), 400
