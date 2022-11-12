import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/init_db', methods=['GET'])
def init_database():

    admin = User('admin', 'admin@example.com')
    print("Data init:")
    print(admin)
    db.create_all() # In case user table doesn't exists already. Else remove it.    
    db.session.add(admin)
    db.session.commit()

    return jsonify('Init Database!')

@app.route('/get_db', methods=['GET'])
def get_database():
    data = User.query.all()
    return jsonify(data[0].username)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run()