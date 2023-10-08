from flask import  request, jsonify, Blueprint
from config import db
from ..models.production import Production, ProductionSchema

production_routes = Blueprint("production_routes", __name__)
production_schema   = ProductionSchema()
production_schemas = ProductionSchema(many=True)

# post
@production_routes.route('/productions', methods=['POST'])
def create():
    user_id = request.json['user_id']
    product_id = request.json['product_id']
    quantity = request.json['quantity']
    date = request.json['date']
    result = Production(user_id, product_id, quantity, date)

    ## example of date format: 2020-01-01 00:00:00

    db.session.add(result)
    db.session.commit()

    return production_schema.jsonify(result)

# # get
@production_routes.route('/productions', methods=['GET'])
def role_list():
    resultall = Production.query.all()
    all_users = production_schemas.dump(resultall)
    return jsonify(all_users)
