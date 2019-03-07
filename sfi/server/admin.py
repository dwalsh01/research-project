from flask import Blueprint, request, jsonify
from .models import NrpSchema, NrpArea
from .common_functions import post_request_full
from flask_login import login_required

#
from flask import send_from_directory, current_app, render_template, abort, flash
from werkzeug.utils import secure_filename
import uuid
import os


bp = Blueprint("admin", __name__, url_prefix="/api")

@bp.route("/nrp", methods=["POST"])
@login_required
def add_nrp():
    return post_request_full(NrpArea, "NRP added")

@bp.route('/nrp', methods=['GET'])
@login_required
def list_nrp():
    nrp = NrpArea.query.all()
    schema = NrpSchema(many=True)
    nrp_areas = schema.dump(nrp)
    return jsonify({"nrp": nrp_areas.data}), 200



def single_file_store(request_file):
    filename = request_file.filename
    pdf = os.path.splitext(filename)[-1] == ".pdf"
    if pdf:
        original_filename = secure_filename(filename)
        random_filename = uuid.uuid4().hex
        up_dir = current_app.config['UPLOAD_FOLDER']
        stored_filename = os.path.join(up_dir, random_filename)
        request_file.save(stored_filename)
        return (stored_filename, filename)
    return

def process_files(request):
    files = []
    for keylist in request.files.listvalues():
        for file in keylist:
            if file.filename:
                file_info = single_file_store(file)
                if file_info:
                    files.append(file_info)
    return files

'''
Testing route for now, to see plain HTML file uploads.

request.files.lists() for a
key --> value map

request.files.listvalues() for a
value list

'''
@bp.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = process_files(request)
        if files:
            for file in files:
                store, filename = file
                print(store, filename)
            return 'files saved', 200
        else:
            return 'either you did not supply a file, or you did not supply a pdf', 400

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=filesx multiple>
      <input type=submit value=Upload>
    </form>
    '''
