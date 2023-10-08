from flask import  request, jsonify, Blueprint
from config import db
from ..models.user import User, UserSchema

user_routes = Blueprint("user_routes", __name__)
user_schema   = UserSchema()
user_schemas = UserSchema(many=True)

# post
@user_routes.route('/users', methods=['POST'])
def create():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    role_id = request.json['role_id']

    result = User(first_name, last_name, role_id)

    db.session.add(result)
    db.session.commit()

    return user_schema.jsonify(result)

# # get
@user_routes.route('/users', methods=['GET'])
def user_list():
    resultall = User.query.all()
    all_users = user_schemas.dump(resultall)
    return jsonify(all_users)
