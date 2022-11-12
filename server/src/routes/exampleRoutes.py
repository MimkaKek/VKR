from flask import Blueprint, jsonify
from ..datatables.user import User
from ..datatables.database import db

exampleBlueprint = Blueprint('exampleBlueprint', __name__)

@exampleBlueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@exampleBlueprint.route('/init_db', methods=['GET'])
def init_database():

    admin = User('admin', 'admin@example.com')
    print("Data init:")
    print(admin)
    db.session.add(admin)
    db.session.commit()

    return jsonify('Init Database!')

@exampleBlueprint.route('/get_db', methods=['GET'])
def get_database():
    data = User.query.all()
    return jsonify(data[0].username)