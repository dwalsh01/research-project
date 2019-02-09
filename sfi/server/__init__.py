import os.path
from os import getenv
from pathlib import PurePath

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sfi.utils import get_project_root


def app_factory(config_param='sfi.server.config.DevelopmentConfig'):
    ''' Initialises the app.

    Initialises the app using the app
    factory pattern.
    '''

    project_root = get_project_root()
    build_partial = 'research-react/build'
    build = project_root.joinpath(build_partial)

    app = Flask(__name__, static_folder=build, instance_relative_config=True)

    app_settings = os.getenv(
        'APP_SETTINGS',
        config_param
    )
    # Configure app from config.py
    app.config.from_object(app_settings)

    # Import and initialise SQLAlchemy
    from sfi.server.models import db, Users

    db.init_app(app)
    migrate = Migrate(app, db)

    # Add db to app configuration
    # (Exposes it to blueprints)
    app.config['DATABASE_OBJ'] = db


    #Blueprints

    # Register playground routes
    from . import playground
    app.register_blueprint(playground.bp)

    from . import auth

    auth.login_manager.init_app(app)
    app.register_blueprint(auth.bp)


    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(f'{build}/{path}'):
            return send_from_directory(build, path)
        else:
            return send_from_directory(build, 'index.html')


    return app