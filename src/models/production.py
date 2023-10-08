from config import db, ma, app
from .role import Role
from sqlalchemy import text
from marshmallow import fields, ValidationError, validates_schema
from ..validations.validation import validate_str, validate_int
from .product import validate_product_id
from .user import validate_no_exist
class Production(db.Model):
    __tablename__ = 'productions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __init__(self, user_id, product_id, quantity, date):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.date = date

with app.app_context():
    db.create_all()

class ProductionSchema(ma.Schema):
    id = fields.Integer(allow_none=False)
    user_id = fields.Integer(required=True, allow_none=False, validate=[validate_int, validate_no_exist])
    product_id = fields.Integer(required=True, allow_none=False, validate=[validate_int, validate_product_id])
    quantity = fields.Integer(required=True, allow_none=False, validate=[validate_int])
    date = fields.Date(required=True, allow_none=False)
    class Meta:
        fields = ('id', 'user_id', 'product_id', 'quantity', 'date')

    # Add custom validation for product_id and user_id
    @validates_schema(skip_on_field_errors=False)
    def validate_product_and_user(self, data, **kwargs):
        product_id = data.get('product_id')
        user_id = data.get('user_id')

        #get the product from the product table
        #check if the kind of the product is valid
        raw_query = text("SELECT LOWER(kind) FROM products WHERE id = :id")
        params = {'id': product_id}
        existing_product = db.session.execute(raw_query, params)
        result1 = existing_product.fetchone()

        #get the role of the user from the user table
        #check if the role of the user is valid
        raw_query = text("SELECT lower(roles.name) FROM users JOIN roles ON roles.id = users.role_id WHERE users.id = :id")
        params = {'id': user_id}
        existing_user = db.session.execute(raw_query, params)
        result2 = existing_user.fetchone()

        if result1[0] != result2[0]:
            raise ValidationError('The product kind is not valid for the user role.')
    
