from src.actions.users import user_routes 
from src.actions.roles import role_routes
from src.actions.products import product_routes
from src.actions.productions import production_routes
from config import app

app.register_blueprint(production_routes)
app.register_blueprint(product_routes)
app.register_blueprint(user_routes)
app.register_blueprint(role_routes)

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')