import os.path
from os import getenv
from sfi.utils import get_project_root
from pathlib import PurePath

from flask import Flask, send_from_directory, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, login_required, login_user, logout_user, current_user
from flask_migrate import Migrate

from passlib.hash import sha256_crypt

def app_factory():
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
        'sfi.server.config.DevelopmentConfig'
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


    login_manager = LoginManager()
    login_manager.init_app(app)


    @login_manager.user_loader
    def user_loader(user_id):
        return Users.query.get(user_id)


    @app.route('/login_user' , methods=['POST'])
    def login():
        content = request.get_json()
        user = Users.query.filter_by(email=content['email']).first()
        if user:
            if sha256_crypt.verify(content['password'], user.password):
                login_user(user, remember=True)
                return jsonify(user.serialize), 200
            else:
                return '', 400



    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("serve"))

    @app.route('/current')
    def current():
        if current_user.is_authenticated:
            return jsonify(current_user.serialize)
        return jsonify({"user": "False"}), 200






    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(f'{build}/{path}'):
            return send_from_directory(build, path)
        else:
            return send_from_directory(build, 'index.html')



    return app
