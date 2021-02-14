from app import *
from moduls.order.Order import Order


class Order(Order, db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    _amount = db.Column(db.Integer)
    date = db.Column(db.String(20))

    def __init__(self, **d):
        super().__init__(**d)


class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'product_id',
                  '_amount', 'date')
