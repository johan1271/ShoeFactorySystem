from flask import Blueprint, request, jsonify
from internal.auth import write_token, validate_token
from config import db
from sqlalchemy import text

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    id = data['id']
    
    if id == "":
        response = jsonify({"message": "Invalid ID"})
        response.status_code = 400
        return response
    
    ##search in the user table for the user_id
    result = db.session.execute(text("SELECT users.id, users.first_name, users.last_name, roles.name FROM users JOIN roles ON roles.id = users.role_id WHERE users.id = :id"), {'id': id})
    result = result.fetchone()

    if result == None:
        response = jsonify({"message": "User not found"})
        response.status_code = 404
        return response
    
    payload = {
        "id": result[0],
        "first_name": result[1],
        "last_name": result[2],
        "role": result[3]
    }

    return jsonify(write_token(payload).decode('utf-8'))

@auth_routes.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)
