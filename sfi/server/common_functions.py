from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

def post_request_full(model, success_message):
    ''' Saves a row to a table.

    Table, and the contents of the row are
    determined by the parameter 'model'.

    Request is assumed to contain a literal
    translation of the object model.
    '''

    post_request = request.get_json()
    if post_request:
        return post_request_short(model, post_request, success_message)
    return jsonify({"status": "failure", "message": "no data provided"}), 400

def post_request_short(model, obj_data, success_message):
    ''' Saves a row to a table.

    Table, and the contents of the row are
    determined by the parameter 'model'.

    Assumed to be passed a dictionary of the
    model.
    '''
    try:
        data = model(**obj_data)
        data.saveToDB()
        response = {
            "status": "success",
            "message": success_message
        }
        return jsonify(response), 201

    except IntegrityError as e:
        short_error = e.orig.diag.message_primary
        invalid_format = {
            "status": "failure",
            "message": "invalid format",
            "error": short_error
        }
        return jsonify(invalid_format), 400
    except TypeError as et:
        error = et
        response = {
            "status": "failure",
            "message": "invalid format",
            "error": str(error)
        }
        return jsonify(response), 400
