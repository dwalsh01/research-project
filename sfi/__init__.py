from os import getcwd
import os.path

from dotenv import load_dotenv
from flask import Flask, send_from_directory, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, login_required, login_user, logout_user, current_user

from passlib.hash import sha256_crypt

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

    # Configure app from config.py
    app.config.from_object('config.DevelopmentConfig')

    # Import and initialise SQLAlchemy
    from . import models

    models.db.init_app(app)

    # Add db to app configuration
    # (Exposes it to blueprints)
    app.config['DATABASE_OBJ'] = models.db

    # Register playground routes
    from . import playground
    app.register_blueprint(playground.bp)


    login_manager = LoginManager()
    login_manager.init_app(app)


    @login_manager.user_loader
    def user_loader(user_id):
        return models.Users.query.get(user_id)


    @app.route('/login_user' , methods=['POST'])
    def login():
        content = request.get_json()
        print(f'hi im content {content}')
        user = models.Users.query.filter_by(email=content['email']).first()
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
        build = 'research-react/build'
        if path != "" and os.path.exists(f'{build}/{path}'):
            return send_from_directory(build, path)
        else:
            return send_from_directory(build, 'index.html')



    return app
