import os
from flask import Blueprint, jsonify, request
from flasgger import swag_from, validate
from sfi.utils import get_project_root
from .models import ProposalCall, LongProposalSchema, ShortProposalSchema
from sqlalchemy.exc import IntegrityError

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
        call = ProposalCall(**post_request)
        try:
            call.saveToDB()
            response = {
                'status': 'success',
                'message': 'call added'
            }
            return jsonify(response), 201

        except IntegrityError as e:
            short_error = e.orig.diag.message_primary
            invalid_format = {
                'status': 'failure',
                'message': 'invalid format',
                'error': short_error
            }
            return jsonify(invalid_format), 400
