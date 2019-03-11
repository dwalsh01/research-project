import os
from flask import Blueprint, jsonify, request
from .models import PendingReviews, PendingReviewsSchema, \
        ProposalApplication, ProposalApplicationSchema, \
        Reviews, Themes, ReviewsSchema
from flask_login import login_required, current_user
from sfi.server.errors.errors import InvalidUsage
from .common_functions import attempt_insert

bp = Blueprint('reviews', __name__, url_prefix="/reviews")

def valid_to_review(uid, app_id):
    valid_user = PendingReviews.query.filter_by(reviewer_id=uid, app_id=app_id).first()
    if valid_user is None:
        raise InvalidUsage("Not authorised to access this page.", status_code=403)

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
    valid_to_review(uid, app_id)
    app = ProposalApplication.query.filter_by(id=app_id).first()
    if app is None:
        raise InvalidUsage(f"App id {app_id} not found", status_code=404)

    schema = ProposalApplicationSchema().dump(app)
    resp = {
        "app": schema.data
    }
    return jsonify(resp)


@bp.route('/add/<int:app_id>', methods=['POST'])
@login_required
def add_review(app_id):
    uid = current_user.id
    #valid_to_review(uid, app_id)

    request_data = request.get_json()
    rating = request_data.get("rating", None)
    if rating is None:
        raise InvalidUsage("Please provide a rating")

    themes = ["quality", "importance", "impact"]
    theme_data = []
    for theme in themes:
        data = request_data.get(theme, None)
        if data is None:
            raise InvalidUsage("Please provide theme: {}".format(theme))
        theme_data.append(data)

    r_data = {
        "rating": rating,
        "app_id": app_id
    }
    review = attempt_insert(Reviews, r_data)

    themes = ["quality", "importance", "impact"]
    for i,theme in enumerate(themes):
        data = {
            "theme_name": theme,
            "theme_critique": theme_data[i],
            "review": review
        }
        attempt_insert(Themes, data)

    resp = {
        "message": "Review submitted"
    }
    return jsonify(resp), 201

@bp.route('/all', methods=['GET'])
def list_reviews():
    reviews = Reviews.query.all()
    review_dump = ReviewsSchema(many=True).dump(reviews)
    if review_dump:
        reviews = review_dump[0]
        for i,review in enumerate(reviews):
            app_id = review["app_id"]
            app = ProposalApplication.query.filter_by(id=app_id).first()
            prop_id = app.proposal_id
            reviews[i]["prop_id"] = prop_id
        return jsonify(reviews)
    return InvalidUsage("No Data available", status_code=404)
