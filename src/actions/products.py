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
    return product_schema.jsonify(result)

# get
@product_routes.route('/products', methods=['GET'])
def product_list():
    resultall = Product.query.all()
    all_users = product_schemas.dump(resultall)
    return jsonify(all_users)


# get by id
@product_routes.route('/products/<int:id>', methods=['GET'])
def product_by_id(id):
    result = Product.query.get(id)
    return product_schema.jsonify(result)

# put
@product_routes.route('/products/<int:id>', methods=['PUT'])
def product_update(id):
    json_data = request.json
    errs = product_schema.validate(json_data)
    if errs:
        return {"error": errs}, 422

    result = Product.query.get(id)
    result.name = json_data['name']
    result.price = json_data['price']
    result.unit_compensation = json_data['unit_compensation']
    result.package_compensation = json_data['package_compensation']
    result.kind = json_data['kind']
    db.session.commit()
    return product_schema.jsonify(result)


# delete
@product_routes.route('/products/<int:id>', methods=['DELETE'])
def product_delete(id):
    result = Product.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return product_schema.jsonify(result)
