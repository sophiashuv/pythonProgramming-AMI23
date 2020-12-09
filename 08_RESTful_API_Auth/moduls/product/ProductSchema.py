from app import *

from moduls.product.Product import *


class Product(Product, db.Model):
    __tablename__ = 'products_new'
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(100), unique=False)
    _price = db.Column(db.Float(), unique=False)
    _image_url = db.Column(db.String(200), unique=False)
    _created_at = db.Column(db.String(20), unique=False)
    _updated_at = db.Column(db.String(20), unique=False)
    description = db.Column(db.String(500), unique=False)
    user_id = db.Column(db.Integer, unique=False)

    def __init__(self, **d):
        super().__init__(**d)


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', '_title', '_price',
                  '_image_url', '_created_at', '_updated_at',
                  'description')