import os
from flask import Flask, send_from_directory, jsonify, request, redirect, url_for
from dotenv import load_dotenv
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_login import login_required, LoginManager, login_required, login_user, logout_user, current_user

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

app = Flask(__name__, static_folder='research-react/build')

app.secret_key = os.environ['SECRET']

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from models import Users, Education

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)

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
    me = Users("matthew", "walsh", "student", "mr", "ltd", "pbkdf2sha256", "252", "mw11@test.com", "password", "131223")
    me.saveToDB()
    return redirect(url_for("serve"))

@app.route('/login_user' , methods=['GET', 'POST'])
def login():
    content = request.get_json()
    user = Users.query.filter_by(email=content['email']).first()
    if user:
        if sha256_crypt.verify(content['password'], user.password):
            login_user(user, remember=True)
            return 'LOGIN SUCCESS'

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'SUCCESSFUL LOGOUT'

@app.route('/current')
def current():
    if current_user.is_authenticated:
        return jsonify(current_user.serialize)
    return 'NO ONE LOGGED IN'

if __name__ == '__main__':
    app.run()