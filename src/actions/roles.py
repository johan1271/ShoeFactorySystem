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
    return role_schema.jsonify(json_data)

# # get
@role_routes.route('/roles', methods=['GET'])
def role_list():
    resultall = Role.query.all()
    all_users = role_schemas.dump(resultall)
    return jsonify(all_users)
