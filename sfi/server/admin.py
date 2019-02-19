from flask import Blueprint


bp = Blueprint('admin', __name__)

@bp.route('/add_nrp', methods=['POST'])
def nrp():
    content = request.get_json()
    print(content)
