from config import db, ma, app

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(15))

    def __init__(self, first_name, last_name, role_id):
        self.first_name = first_name
        self.last_name = last_name
        self.role_id = role_id

    

with app.app_context():
    db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'role_id', 'first_name', 'last_name')

