from config import db, ma, app
from .role import Role
from sqlalchemy import text
from marshmallow import fields, ValidationError
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

