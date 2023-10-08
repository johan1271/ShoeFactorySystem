from config import db, ma, app
from marshmallow import fields, ValidationError
from ..validations.validation import validate_str
from sqlalchemy import text

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

with app.app_context():
    db.create_all()

def validate_name(val):
    #check if role_id exists in roles table
    #converrt to lowercase
    val = val.lower()
    raw_query = text("SELECT EXISTS(SELECT 1 FROM roles WHERE LOWER(name) = :name)") 
    params = {'name': val}

    existing_role = db.session.execute(raw_query, params)
    row = existing_role.fetchone()

    if row[0] == 1:
        raise ValidationError('Role already exists.')

class RoleSchema(ma.Schema):
    id = fields.Integer( allow_none=False)
    name = fields.Str(required=True, allow_none=False, validate=[validate_str, validate_name])
    class Meta:
        fields = ('id', 'name')
