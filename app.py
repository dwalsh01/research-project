import os
from flask import Flask, send_from_directory, jsonify, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

app = Flask(__name__, static_folder='research-react/build')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Users, Education

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
    me = Users("moyra", "walsh","staff", "mrs. ", "phd", "12313123", 445, "moyra@gmail.com", "asdaf1")
    db.session.add(me)
    db.session.commit()
    res = Users.query.filter_by(f_name='daragh').first()
    return str(res.f_name)


if __name__ == '__main__':
    app.run()