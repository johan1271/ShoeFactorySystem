from config import db, ma, app
from sqlalchemy import text
from marshmallow import fields

class UserProduction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    name = db.Column(db.String(50))
    unit_compensation = db.Column(db.Float)
    package_compensation = db.Column(db.Float)
    total_quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    price = db.Column(db.Integer)

    def __init__(self, first_name, last_name, name, unit_compensation, package_compensation, total_quantity, date, price):
        self.first_name = first_name
        self.last_name = last_name
        self.name = name
        self.unit_compensation = unit_compensation
        self.package_compensation = package_compensation
        self.total_quantity = total_quantity
        self.date = date
        self.price = price

    def package_calculation(production):
        new = {}

        #calculate the price of the package
        packagePrice = 12 * production['price']

        #calculate the compensation is a percentage of the price
        packageCompensation = packagePrice * (production['package_compensation'] / 100)

        #add the package compensation to the object
        new['compensation'] = packageCompensation
        new['price'] = packagePrice
        new["name"] = production['name']
        new["quantity"] = 12
        new["unit_price"] = production['price']
        new["percentage"] = production['package_compensation']
        new["employee_name"] = production['first_name'] + " " + production['last_name']
    
        return new

    def unit_calculation(production, remaining):
        #add it as a separate object to the production object
        new = {}
        remainingPrice = remaining * production['price']
        new['compensation'] = remainingPrice * (production['unit_compensation'] / 100)
        new['price'] = remainingPrice
        new["name"] = production['name']
        new["quantity"] = remaining
        new["unit_price"] = production['price']
        new["percentage"] = production['unit_compensation']
        new["employee_name"] = production['first_name'] + " " + production['last_name']

        return new

    def build_final_object(production, final_object, production_object):
        production['unit_compensation'] = float(production['unit_compensation'])
        production['package_compensation'] = float(production['package_compensation'])
        production['total_quantity'] = int(production['total_quantity'])
        production['date'] = str(production['date'])
        production['price'] = int(production['price'])

        if production['total_quantity'] > 12:
            new = UserProduction.package_calculation(production)
            final_object.append(new)
            remaining = production['total_quantity'] % 12
        
            if remaining > 0:
                new = UserProduction.unit_calculation(production, remaining)
                final_object.append(new)

        elif production['total_quantity'] == 12:
            new = UserProduction.package_calculation(production)
            final_object.append(new)

        else:
            remaining = production['total_quantity']
            new = UserProduction.unit_calculation(production, remaining)
            final_object.append(new)

        production_object['production'] = final_object

    def ByUser(user_id, start_date, end_date):
        if start_date == None:
            start_date = '1900-01-01'
        
        if end_date == None:
            end_date = '2100-01-01'

        result = db.session.execute(text('''
        SELECT 
            SUM(productions.quantity) AS total_quantity,
            users.first_name,
            users.last_name,
            productions.date,
            products.name,
            products.unit_compensation,
            products.package_compensation,
            products.price 
        FROM productions 
        JOIN products ON products.id = productions.product_id 
        JOIN users ON users.id = productions.user_id 
        WHERE users.id = :user_id 
        AND 
            productions.date
        BETWEEN
            :start_date
        AND
            :end_date
        GROUP BY users.first_name, users.last_name, productions.date, products.name, products.id;'''), {'user_id': user_id, 'start_date': start_date, 'end_date': end_date})
        
        schema = UserProductionSchema(many=True)
        all_production = schema.dump(result)
        user_production_object = {}
        package_object = []
        for production in all_production:
            production['unit_compensation'] = float(production['unit_compensation'])
            production['package_compensation'] = float(production['package_compensation'])
            production['total_quantity'] = int(production['total_quantity'])
            production['date'] = str(production['date'])
            production['price'] = int(production['price'])

            UserProduction.build_final_object(production, package_object, user_production_object)
            user_production_object['total_compensation'] = sum([x['compensation'] for x in package_object])

        return user_production_object

    def All(start_date, end_date):
        if start_date == None:
            start_date = '1900-01-01'

        if end_date == None:
            end_date = '2100-01-01'
            
        result = db.session.execute(text('''
            SELECT 
                SUM(productions.quantity) AS total_quantity,
                users.first_name,
                users.last_name,
                productions.date,
                products.name,
                products.unit_compensation,
                products.package_compensation,
                products.price 
            FROM productions 
            JOIN products ON products.id = productions.product_id 
            JOIN users ON users.id = productions.user_id 
            WHERE 
                productions.date
            BETWEEN
                :start_date 
            AND 
                :end_date
            GROUP BY users.first_name, users.last_name, productions.date, products.name, products.id;'''), {'start_date': start_date, 'end_date': end_date})
        
        schema = UserProductionSchema(many=True)
        all_production = schema.dump(result)
        production_object = {}
        package_object = []
        for production in all_production:
            UserProduction.build_final_object(production, package_object, production_object)

        return production_object

class UserProductionSchema(ma.Schema):
    id = fields.Integer(allow_none=False)
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)
    name = fields.Str(required=True, allow_none=False)
    unit_compensation = fields.Float(required=True, allow_none=False)
    package_compensation = fields.Float(required=True, allow_none=False)
    total_quantity = fields.Integer(required=True, allow_none=False)
    date = fields.Date(required=True, allow_none=False)
    price = fields.Integer(required=True, allow_none=False)
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'name', 'unit_compensation', 'package_compensation', 'total_quantity', 'date', 'price')