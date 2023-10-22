from flask import  request, jsonify, Blueprint
from config import db
from ..models.production import Production, ProductionSchema
from ..models.user_production import UserProduction, UserProductionSchema
production_routes = Blueprint("production_routes", __name__)
production_schema   = ProductionSchema()
production_schemas = ProductionSchema(many=True)
from sqlalchemy import text
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



# put
@production_routes.route('/productions/<int:id>', methods=['PUT'])
def update(id):
    json_data = request.json
    errs = production_schema.validate(json_data)
    if errs:
        return {"error": errs}, 422

    result = Production.query.get(id)
    result.user_id = json_data['user_id']
    result.product_id = json_data['product_id']
    result.quantity = json_data['quantity']
    result.date = json_data['date']
    db.session.commit()
    return production_schema.jsonify(result)

# get by id
@production_routes.route('/productions/<int:id>', methods=['GET'])
def production_by_id(id):
    result = db.session.execute(text("""
    SELECT 
        productions.id,
        users.first_name,
        users.last_name,
        roles.name AS role,
        quantity,
        productions.date,
        productions.product_id,
        productions.user_id,
        products.name AS product_name
    from productions
    JOIN products ON products.id = productions.product_id
    JOIN users ON users.id = productions.user_id
    JOIN roles ON roles.id = users.role_id
    WHERE productions.id = :id"""), {'id': id})
    result = result.fetchone()
    
    json = {
        "id": result[0],
        "user_first_name": result[1],
        "user_last_name": result[2],
        "user_role": result[3],
        "quantity": result[4],
        "date": result[5],
        "product_id": result[6],
        "user_id": result[7],
        "product_name": result[8]
    }

    return jsonify(json)

# # get
@production_routes.route('/productions/<int:user_id>', methods=['GET'])
@production_routes.route('/productions', methods=['GET'])
def production_list(user_id=None):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if user_id == None:
        resultall = UserProduction.All(start_date, end_date)
        return jsonify(resultall)

    resultall = UserProduction.ByUser(user_id, start_date, end_date)

    return jsonify(resultall)


@production_routes.route('/productions/<int:id>', methods=['DELETE'])
def production_delete(id):
    result = Production.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return production_schema.jsonify(result)


@production_routes.route('/all_productions', methods=['GET'])
def all_productions():
    result = db.session.execute(text("""
    SELECT 
        productions.id,
        users.first_name,
        users.last_name,
        roles.name AS role,
        quantity,
        productions.date,
        productions.product_id,
        productions.user_id,
        products.name AS product_name
    from productions
    JOIN products ON products.id = productions.product_id
    JOIN users ON users.id = productions.user_id
    JOIN roles ON roles.id = users.role_id"""))
    result = result.fetchall()

    json = []
    for production in result:
        new = {
            "id": production[0],
            "user_first_name": production[1],
            "user_last_name": production[2],
            "user_role": production[3],
            "quantity": production[4],
            "date": production[5],
            "product_id": production[6],
            "user_id": production[7],
            "product_name": production[8]
        }
        json.append(new)

    return jsonify(json)
