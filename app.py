from src.actions.users import user_routes 
from src.actions.roles import role_routes
from src.actions.products import product_routes
from src.actions.productions import production_routes
from src.actions.auth import auth_routes
from config import app
from dotenv import load_dotenv
from flask_cors import CORS
from flask import request, jsonify
from internal.auth import validate_token
app.register_blueprint(auth_routes)

##add a middleware to check if the user is logged in
@product_routes.before_request
@production_routes.before_request
@user_routes.before_request
@role_routes.before_request
def check_if_logged_in():
    token = request.headers['Authorization'].split(" ")[1]
    if token == None:
        response = jsonify({"message": "Token not found"})
        response.status_code = 404
        return response
    return validate_token(token, output=False)

app.register_blueprint(production_routes)
app.register_blueprint(product_routes)
app.register_blueprint(user_routes)
app.register_blueprint(role_routes)

CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, port=8080, host='0.0.0.0')