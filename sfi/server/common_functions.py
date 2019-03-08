from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from sfi.server.errors.errors import InvalidUsage

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
    raise InvalidUsage("No JSON data provided")

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
        raise InvalidUsage(e.orig.diag.message_primary)

    except TypeError as et:
        raise InvalidUsage(str(et))

def attempt_insert(model, obj_data):
    ''' Attempts to insert and save a model.

    '''
    try:
        data = model(**obj_data)
        data.saveToDB()
        return data

    except IntegrityError as e:
        raise InvalidUsage(e.orig.diag.message_primary)

    except TypeError as error:
        raise InvalidUsage(str(error))

def attempt_save(model):
    try:
        model.saveToDB()
        return model

    except IntegrityError as e:
        raise InvalidUsage(e.orig.diag.message_primary)

    except TypeError as error:
        raise InvalidUsage(str(error))
