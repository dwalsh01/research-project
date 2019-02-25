from flask import Blueprint, request, jsonify
from .models import NrpSchema, NrpArea
from .common_functions import post_request_full

bp = Blueprint("admin", __name__, url_prefix="/api")

@bp.route("/nrp", methods=["POST"])
def add_nrp():
    return post_request_full(NrpArea, "NRP added")

@bp.route('/nrp', methods=['GET'])
def list_nrp():
    nrp = NrpArea.query.all()
    schema = NrpSchema(many=True)
    nrp_areas = schema.dump(nrp)
    return jsonify({"nrp": nrp_areas.data}), 200
