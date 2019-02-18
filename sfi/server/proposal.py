import os
from flask import Blueprint, jsonify, request
from flasgger import swag_from, validate
from sfi.utils import get_project_root
from .models import ProposalCall

swagger_prop = os.path.join(get_project_root(), "swagger", "api-proposal.yml")
bp = Blueprint('proposal', __name__, url_prefix="/calls")

@bp.route('/list')
@swag_from(swagger_prop, methods=['GET'])
def list_proposals():
    proposals = ProposalCall.query.all()
    print(proposals)
    return jsonify(proposals)

@bp.route('/show/<id>')
def show_proposal():
    pass


@bp.route('/add', methods=['POST'])
def add_proposal():
    post_request = request.get_json()
