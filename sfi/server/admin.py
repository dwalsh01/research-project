from flask import Blueprint, request, jsonify
from .models import NrpSchema, NrpArea
from .common_functions import post_request_full
from flask_user import roles_required

bp = Blueprint("admin", __name__, url_prefix="/api")

@bp.route("/nrp", methods=["POST"])
@roles_required('admin')
def add_nrp():
    return post_request_full(NrpArea, "NRP added")

@bp.route('/nrp', methods=['GET'])
@roles_required('admin')
def list_nrp():
    nrp = NrpArea.query.all()
    schema = NrpSchema(many=True)
    nrp_areas = schema.dump(nrp)
    return jsonify({"nrp": nrp_areas.data}), 200
