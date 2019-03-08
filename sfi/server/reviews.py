import os
from flask import Blueprint, jsonify, request
from .models import PendingReviews, PendingReviewsSchema
from flask_login import login_required, current_user
from sfi.server.errors.errors import InvalidUsage

bp = Blueprint('proposal', __name__, url_prefix="/reviews")

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
@bp.route('/pending')
@login_required
def pending_reviews():
    uid = current_user.id
    pendingreviews = PendingReviews.filter_by(reviewer_id=user_id)
    if pendingreviews is None:
        raise InvalidUsage("No reviews found", status_code=404)
    schema = PendingReviewsSchema.dump(pending_reviews, many=True)
    print(schema)
    return schema.jsonify(pendingreview)
