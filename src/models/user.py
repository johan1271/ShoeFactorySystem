from config import db, ma, app
from .role import Role
from sqlalchemy import text
from marshmallow import fields, ValidationError
from ..validations.validation import validate_str, validate_int
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(15))
    active = db.Column(db.Boolean)

    def __init__(self, id, first_name, last_name, role_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.role_id = role_id
        self.active = True

with app.app_context():
    db.create_all()

def validate_role_id(val):
    #check if role_id exists in roles table
    existing_role = db.session.query(Role).filter_by(id=val).first()

    if existing_role is None:
        raise ValidationError('Role does not exist.')
    

def validate_user_id(val):
    #check if user_id exists in users 
    raw_query = text("SELECT EXISTS(SELECT 1 FROM users WHERE id = :id)") 
    params = {'id': val}

    existing_user = db.session.execute(raw_query, params)
    row = existing_user.fetchone()

    if row[0] == 1:
        raise ValidationError('User already exists.')

def validate_no_exist(val):
    #check if user_id exists in users 
    raw_query = text("SELECT EXISTS(SELECT 1 FROM users WHERE id = :id)") 
    params = {'id': val}

    existing_user = db.session.execute(raw_query, params)
    row = existing_user.fetchone()

    if row[0] == 0:
        raise ValidationError('User does not exist.')

class UserSchema(ma.Schema):
    id = fields.Integer(required=True, allow_none=False, validate=[validate_int, validate_user_id])
    role_id = fields.Integer(required=True, allow_none=False, validate=[validate_int, validate_role_id])
    first_name = fields.Str(required=True, allow_none=False, validate=validate_str)
    last_name = fields.Str(required=True, allow_none=False, validate=validate_str)
    active = fields.Boolean(allow_none=False, default=True)
    class Meta:
        fields = ('id', 'role_id', 'first_name', 'last_name', 'active')
