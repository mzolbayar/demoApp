from flask import Flask, request,  jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask_cors import CORS
app = Flask(__name__)

CONN_STR='mysql+mysqlconnector://{username}@{host}:{port}/{database_name}'.format(
    username="root",
    host="localhost",
    port="3306",
    database_name="DemoApp"
)

app.config['SQLALCHEMY_DATABASE_URI'] = CONN_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

class UserInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.name}>'

def setup_db():
    with app.app_context():
        db.create_all()

#Create user
@app.route('/user', methods=['POST'])
def add_user():
    print(request)
    name = request.json.get('name')
    email = request.json.get('email')

    user = UserInformation(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "New user added", "user_id": user.id}), 200

#Update user
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = UserInformation.query.get(user_id)

    name = request.json.get('name')
    email = request.json.get('email')

    if name:
        user.name = name

    if email:
        user.email = email

    db.session.commit()
    
    return jsonify({'message': 'User updated', 'user_id': user.id}), 200

#Delete user
@app.route('/user/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    user = UserInformation.query.get(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted', 'user_id': user.id}), 200
    
if __name__ == '__main__':
    setup_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    
    