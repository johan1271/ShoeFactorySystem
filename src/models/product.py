from config import db, ma, app

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    unit_compensation = db.Column(db.Float)
    package_compensation = db.Column(db.Float)

    def __init__(self, name, price, unit_compensation, package_compensation):
        self.name = name
        self.price = price
        self.unit_compensation = unit_compensation
        self.package_compensation = package_compensation

with app.app_context():
    db.create_all()

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'unit_compensation', 'package_compensation')
