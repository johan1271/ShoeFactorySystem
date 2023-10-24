from flask import  request, jsonify, Blueprint
from config import db
from ..models.role import Role, RoleSchema

role_routes = Blueprint("role_routes", __name__)
role_schema   = RoleSchema()
role_schemas = RoleSchema(many=True)

# post
@role_routes.route('/roles', methods=['POST'])
def create():
    json_data = request.json
    errs = role_schema.validate(json_data)
    if errs:
        return {"error": errs}, 422

    result = Role(json_data['name'])
    db.session.add(result)
    db.session.commit()
    return role_schema.jsonify(result)

# # get
@role_routes.route('/roles', methods=['GET'])
def role_list():
    resultall = Role.query.all()
    all_users = role_schemas.dump(resultall)
    return jsonify(all_users)

# get by id
@role_routes.route('/roles/<int:id>', methods=['GET'])
def role_by_id(id):
    result = Role.query.get(id)
    return role_schema.jsonify(result)

# put
@role_routes.route('/roles/<int:id>', methods=['PUT'])
def role_update(id):
    json_data = request.json
    errs = role_schema.validate(json_data)
    if errs:
        return {"error": errs}, 422

    result = Role.query.get(id)
    result.name = json_data['name']
    db.session.commit()
    return role_schema.jsonify(result)

# delete
@role_routes.route('/roles/<int:id>', methods=['DELETE'])
def role_delete(id):
    result = Role.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return role_schema.jsonify(result)
