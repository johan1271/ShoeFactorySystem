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
    resultall = User.query.all()
    all_users = user_schemas.dump(resultall)
    return jsonify(all_users)
