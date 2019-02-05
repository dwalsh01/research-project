from os import getcwd, getenv
import os.path

from dotenv import load_dotenv
from flask import Flask, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy

def app_factory():
    ''' Initialises the app.

    `cwd` is a bit finicky at the moment.
    (If running normally, it will point to
    the parent directory of this file.
    '''

    # Load environment variables
    cwd = getcwd()
    env_path = os.path.join(cwd, ".env")
    load_dotenv(env_path, verbose=True)


    app = Flask(__name__, static_folder="research-react/build", root_path=cwd)

    # Configure app
    app.config.from_object(getenv('APP_SETTINGS', 'config.Config'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Import and initialise SQLAlchemy
    from . import models

    models.db.init_app(app)



    sampleData = [
        {"grant_id": 0, "grant_title": 'Sample title 1'},
        {"grant_id": 1, "grant_title": 'Sample title 2'},
        {"grant_id": 2, "grant_title": 'Sample title 3'}
     ]


    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists("research-react/build/" + path):
            return send_from_directory('research-react/build', path)
        else:
            return send_from_directory('research-react/build', 'index.html')

    @app.route('/testing', methods=['GET'])
    def testing():
        if request.method == 'GET':
            return jsonify(sampleData)

    @app.route('/insert_user')
    def insert_user():
        me = models.Users("moyra", "walsh","staff", "mrs. ", "phd", "12313123", 445, "moyra@gmail.com", "asdaf1")
        models.db.session.add(me)
        models.db.session.commit()
        res = models.Users.query.filter_by(f_name='daragh').first()
        return str(res.f_name)


    return app
