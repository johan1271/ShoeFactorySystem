from flask import  request, jsonify, Blueprint
from config import db
from ..models.user import User, UserSchema
from marshmallow import ValidationError

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
    return user_schema.jsonify(json_data)

# get
@user_routes.route('/users', methods=['GET'])
def user_list():
    resultall = User.query.filter(User.active == True).all()
    all_users = user_schemas.dump(resultall)
    return jsonify(all_users)

# get by id
@user_routes.route('/users/<int:id>', methods=['GET'])
def user_by_id(id):
    result = User.query.get(id)
    return user_schema.jsonify(result)

# put
@user_routes.route('/users/<int:id>', methods=['PUT'])
def user_update(id):
    json_data = request.json
    errs = user_schema.validate(json_data)
    if errs:
        return {"error": errs}, 422

    result = User.query.get(id)
    result.first_name = json_data['first_name']
    result.last_name = json_data['last_name']
    result.role_id = json_data['role_id']
    db.session.commit()
    return user_schema.jsonify(json_data)


# delete
@user_routes.route('/users/<int:id>', methods=['DELETE'])
def user_delete(id):
    result = User.query.get(id)
    result.active = False
    db.session.commit()
    return user_schema.jsonify(result)