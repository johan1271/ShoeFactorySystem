from config import db, ma, app
from marshmallow import fields, ValidationError
from ..validations.validation import validate_str, validate_int, validate_float
from sqlalchemy import text
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    unit_compensation = db.Column(db.Float)
    package_compensation = db.Column(db.Float)
    kind = db.Column(db.String(50))

    def __init__(self, name, price, unit_compensation, package_compensation, kind):
        self.name = name
        self.price = price
        self.unit_compensation = unit_compensation
        self.package_compensation = package_compensation
        self.kind = kind

with app.app_context():
    db.create_all()


def validate_product(val):
    #check if product_name exisrs in products table
    #converrt to lowercase
    val = val.lower()
    raw_query = text("SELECT EXISTS(SELECT 1 FROM products WHERE LOWER(name) = :name)")
    params = {'name': val}

    existing_product = db.session.execute(raw_query, params)
    row = existing_product.fetchone()

    if row[0] == 1:
        raise ValidationError('Product already exists.')
    
def validate_product_id(val):
    #check if product_id exists in products 
    raw_query = text("SELECT EXISTS(SELECT 1 FROM products WHERE id = :id)") 
    params = {'id': val}

    existing_product = db.session.execute(raw_query, params)
    row = existing_product.fetchone()

    if row[0] == 0:
        raise ValidationError('Product does not exist.')

def validate_kind(val):
    #check if kind is valid
    val = val.lower()
    if val != 'guarnecedor' and val != 'cortador' and val != 'ensamblador':
        raise ValidationError('Kind is not valid.')

class ProductSchema(ma.Schema):
    id = fields.Integer(allow_none=False)
    name = fields.Str(required=True, allow_none=False, validate=[validate_str, validate_product])
    price = fields.Integer(required=True, allow_none=False, validate=validate_int)
    unit_compensation = fields.Float(required=True, allow_none=False, validate=validate_float)
    package_compensation = fields.Float(required=True, allow_none=False, validate=validate_float)
    kind = fields.Str(required=True, allow_none=False, validate=[validate_str, validate_kind])
    class Meta:
        fields = ('id', 'name', 'price', 'unit_compensation', 'package_compensation', 'kind')
