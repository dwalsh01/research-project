from os import getcwd, getenv
import os.path

from dotenv import load_dotenv
from flask import Flask, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy

def app_factory():
    ''' Initialises the app.

    `cwd` is a bit finicky at the moment.
    (If running normally, it will point to
    the parent directory of this file).
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

    # Add db to app configuration
    # (Exposes it to blueprints)

    app.config['DATABASE_OBJ'] = models.db

    # Register playground routes
    from . import playground
    app.register_blueprint(playground.bp)

    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        build = 'research-react/build'
        if path != "" and os.path.exists(f'{build}/{path}'):
            return send_from_directory(build, path)
        else:
            return send_from_directory(build, 'index.html')


    return app
