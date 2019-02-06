from flask import Blueprint, current_app, jsonify, send_from_directory, request
from . import models

bp = Blueprint('playground', __name__, url_prefix="/playground")


sampleData = [
    {"grant_id": 0, "grant_title": 'Sample title 1'},
    {"grant_id": 1, "grant_title": 'Sample title 2'},
    {"grant_id": 2, "grant_title": 'Sample title 3'}
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
    me = models.Users("moyra", "walsh","staff", "mrs. ", "phd", "12313123", 445, "moyra@gmail.com", "asdaf1")
    db.session.add(me)
    db.session.commit()
    res = models.Users.query.filter_by(f_name='daragh').first()
    return str(res.f_name)



@bp.route('/testing', methods=['GET'])
def testing():
    if request.method == 'GET':
        return jsonify(sampleData)

