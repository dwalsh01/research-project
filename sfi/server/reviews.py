import os
from flask import Blueprint, jsonify, request
from .models import PendingReviews, PendingReviewsSchema, \
        ProposalApplication, ProposalApplicationSchema
from flask_login import login_required, current_user
from sfi.server.errors.errors import InvalidUsage

bp = Blueprint('reviews', __name__, url_prefix="/reviews")

'''
Should list all of the reviews pending
for the user 'user_id'

What it should do:
Query the database for the PendingReviews table
filter for just this user (reviewer_id = user_id)

output:
JSON of:

the PendingReviews table

'''
@bp.route('/pending', methods=['GET'])
@login_required
def pending_reviews():
    print("route hit")
    uid = current_user.id
    pending_reviews = PendingReviews.query.filter_by(reviewer_id=uid).all()
    if len(pending_reviews) == 0:
        raise InvalidUsage("No reviews found", status_code=404)

    schema = PendingReviewsSchema(many=True).dump(pending_reviews)
    resp = {
        "reviews": schema.data
    }
    return jsonify(resp)

@bp.route("/pending/<int:app_id>")
@login_required
def view_app(app_id):
    uid = current_user.id
    valid_user = PendingReviews.query.filter_by(reviewer_id=uid, app_id=app_id).first()
    if valid_user is None:
        raise InvalidUsage("Not authorised to access this page.", status_code=403)

    app = ProposalApplication.query.filter_by(id=app_id).first()
    if app is None:
        raise InvalidUsage(f"App id {app_id} not found", status_code=404)

    schema = ProposalApplicationSchema().dump(app)
    resp = {
        "app": schema.data
    }
    return jsonify(resp)
