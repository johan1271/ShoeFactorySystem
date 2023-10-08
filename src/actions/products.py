from flask import  request, jsonify, Blueprint
from config import db
from ..models.product import Product, ProductSchema

product_routes = Blueprint("product_routes", __name__)
product_schema   = ProductSchema()
product_schemas = ProductSchema(many=True)

# post
@product_routes.route('/products', methods=['POST'])
def create():
    json_data = request.json
    errs = product_schema.validate(json_data)
    if errs:
        return {"error": errs}, 422

    result = Product(json_data['name'],json_data['price'], json_data['unit_compensation'], json_data['package_compensation'], json_data['kind'])
    db.session.add(result)
    db.session.commit()
    return product_schema.jsonify(json_data)

# get
@product_routes.route('/products', methods=['GET'])
def product_list():
    resultall = Product.query.all()
    all_users = product_schemas.dump(resultall)
    return jsonify(all_users)
