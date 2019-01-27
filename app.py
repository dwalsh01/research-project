import os
from flask import Flask, send_from_directory, jsonify, request
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

app = Flask(__name__, static_folder='research-react/build')

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

if __name__ == '__main__':
    app.run()