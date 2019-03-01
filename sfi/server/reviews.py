import os
from flask import Blueprint, jsonify, request
from .models import PendingReviews, PendingReviewsSchema

bp = Blueprint('proposal', __name__, url_prefix="/reviews")

'''
Should list all of the reviews pending
for the user 'user_id'

Input: "user_id"

What it should do:
Query the database for the PendingReviews table
filter for just this user (reviewer_id = user_id)

output:
JSON of:

the PendingReviews table

'''
@bp.route('/pending/<int:user_id')
def pending_reviews(user_id):
    pendingreview = PendingReviews.filter_by(reviewer_id=user_id)
    if pendingreview is None:
        return '', 404
    schema = PendingReviewsSchema()
    return schema.jsonify(pendingreview)
