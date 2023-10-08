from flask import  request, jsonify, Blueprint
from config import db
from ..models.product import Product, ProductSchema

product_routes = Blueprint("product_routes", __name__)
product_schema   = ProductSchema()
product_schemas = ProductSchema(many=True)

# post
@product_routes.route('/products', methods=['POST'])
def create():
    name = request.json['name']
    price = request.json['price']
    unit_compensation = request.json['unit_compensation']
    package_compensation = request.json['package_compensation']
    result = Product(name, price, unit_compensation, package_compensation)

    db.session.add(result)
    db.session.commit()

    return product_schema.jsonify(result)

# # get
@product_routes.route('/products', methods=['GET'])
def product_list():
    resultall = Product.query.all()
    all_users = product_schemas.dump(resultall)
    return jsonify(all_users)
