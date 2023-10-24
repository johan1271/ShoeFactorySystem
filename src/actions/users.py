from flask import  request, jsonify, Blueprint
from config import db
from ..models.user import User, UserSchema
from marshmallow import ValidationError
from sqlalchemy import text
import json

user_routes = Blueprint("user_routes", __name__)
user_schema   = UserSchema()
user_schemas = UserSchema(many=True)

# post
@user_routes.route('/users', methods=['POST'])
def create():
    json_data = request.json
    errs = user_schema.validate(json_data)
    if errs:
        return {"error": errs}, 422

    result = User(json_data['id'],json_data['first_name'], json_data['last_name'], json_data['role_id'])
    db.session.add(result)
    db.session.commit()
    return user_schema.jsonify(result)

# get
@user_routes.route('/users', methods=['GET'])
def user_list():
    result = db.session.execute(text("""
        SELECT users.id,
        users.first_name,
        users.last_name,
        roles.name,
        roles.id,
        users.active
        FROM users JOIN roles ON roles.id = users.role_id"""))
    resultall = result.fetchall()
    
    all_users = []
    for user in resultall:
        json = {
            "id": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "role": user[3],
            "role_id": user[4],
            "active": user[5]
        }
        all_users.append(json)
        
    
    return jsonify(all_users)

# get by id
@user_routes.route('/users/<int:id>', methods=['GET'])
def user_by_id(id):
    ##search in the role table for the role_id and return the name
    result = db.session.execute(text("""
        SELECT users.id, 
        users.first_name, 
        users.last_name, 
        roles.name,
        roles.id,
        users.active
        FROM users JOIN roles ON roles.id = users.role_id WHERE users.id = :id"""), {'id': id})
    result = result.fetchone()

    json = {
        "id": result[0],
        "first_name": result[1],
        "last_name": result[2],
        "role": result[3],
        "role_id": result[4],
        "active": result[5]
    }
    return jsonify(json)

# put
@user_routes.route('/users/<int:id>', methods=['PUT'])
def user_update(id):
    json_data = request.json
    

    result = User.query.get(id)
    result.id = json_data['id']
    result.first_name = json_data['first_name']
    result.last_name = json_data['last_name']
    result.role_id = json_data['role_id']
    result.active = json_data['active']
    db.session.commit()
    return user_schema.jsonify(result)


# delete
@user_routes.route('/users/<int:id>', methods=['DELETE'])
def user_delete(id):
    result = User.query.get(id)
    result.active = False
    db.session.commit()
    return user_schema.jsonify(result)
