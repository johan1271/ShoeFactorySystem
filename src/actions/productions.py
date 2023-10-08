from flask import  request, jsonify, Blueprint
from config import db
from ..models.production import Production, ProductionSchema
from ..models.user_production import UserProduction, UserProductionSchema
production_routes = Blueprint("production_routes", __name__)
production_schema   = ProductionSchema()
production_schemas = ProductionSchema(many=True)

# post
@production_routes.route('/productions', methods=['POST'])
def create():
    ## example of date format: 2020-01-01 00:00:00
    json_data = request.json
    errs = production_schema.validate(json_data)
    if errs:
        return {"error": errs}, 422

    result = Production(json_data['user_id'],json_data['product_id'], json_data['quantity'], json_data['date'])
    db.session.add(result)
    db.session.commit()
    return production_schema.jsonify(result)

# # get
@production_routes.route('/productions/<int:user_id>', methods=['GET'])
@production_routes.route('/productions', methods=['GET'])
def production_list(user_id=None):
    if user_id == None:
        resultall = Production.query.all()
        all_users = production_schemas.dump(resultall)
        return jsonify(all_users)

    resultall = UserProduction.ByUser(user_id)

    return jsonify(resultall)
