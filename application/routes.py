from application import app,db
from flask import request, jsonify
from application.models import User

def insert_initial_users():
        
        user1 = User(first_name='Josh', last_name='Doe', email='john.doe@example.com', age=30)
        user2 = User(first_name='Jane', last_name='Smith', email='jane.smith@example.com', age=25)

        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()

def format_user(user):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "id": user.id
    }

#POST /init_users (populate db with sample data)
@app.route('/init_users', methods=['POST'])
def initialize_users():
    insert_initial_users()
    return jsonify(message='Initial users inserted successfully!'), 201

#GET /
@app.route("/")
def welcome():
    return "<p>Welcome to my API<p>"

#GET, POST /users
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        data = request.json
        user = User(data["first_name"], data["last_name"], data["email"], data["age"])
        db.session.add(user)
        db.session.commit()
        return jsonify(id=user.id, first_name=user.first_name, last_name=user.last_name, age=user.age)
    elif request.method == "GET":
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append(format_user(user))
        return user_list
    
# GET /:id
@app.route('/users/<id>')
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email, age=user.age)

#DELETE /:id
@app.route('/users/<id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify(message='User not found'), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify(message='User deleted successfully'), 200

#PATCH /:id 
@app.route('/users/<int:id>', methods=["PATCH"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json

    for key, value in data.items():
        setattr(user, key, value)

    db.session.commit()
    return jsonify(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email, age=user.age)
