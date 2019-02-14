from flask import Blueprint, current_app, jsonify, send_from_directory, request, redirect, url_for
from . import models

bp = Blueprint('playground', __name__, url_prefix="/playground")


sampleData = [
    {"grant_id": 0, "grant_title": 'Brussels Conference Programme'},
    {"grant_id": 1, "grant_title": 'SFI Frontiers for Future Programme'},
    {"grant_id": 2, "grant_title": 'SFI Discover Programme'},
    {"grand_id": 3, "grant_title": 'US-Ireland R&D Programme'}
 ]

db_config = "DATABASE_OBJ"


@bp.record
def record(state):
    '''Initialises blueprint

    This record checks for the existence
    of the database object.

    The .record decorator makes this function
    run when this blueprint is initialised.
    '''
    db = state.app.config.get(db_config)
    if db is None:
        raise Exception("No {db_config} set in configuration.")


@bp.route('/insert_user')
def insert_user():
    db = current_app.config[db_config]
    me = models.Users("matthew", "walsh", "student", "mr", "ltd",
                      "pbkdf2sha256", "252", "mw11@test.com", "password", "131223")

    me.saveToDB()
    return redirect(url_for("serve"))



@bp.route('/testing', methods=['GET'])
def testing():
    if request.method == 'GET':
        return jsonify(sampleData)

