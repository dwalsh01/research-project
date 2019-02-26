import os
from flask import Blueprint, jsonify, request

bp = Blueprint('proposal', __name__, url_prefix="/reviews")

'''
Should list all of the reviews pending
for the user 'user_id'
'''
@bp.route('/pending/<int:user_id')
def pending_reviews(user_id):
    pass

