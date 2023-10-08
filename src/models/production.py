from config import db, ma, app

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
    class Meta:
        fields = ('id', 'user_id', 'product_id', 'quantity', 'date')

