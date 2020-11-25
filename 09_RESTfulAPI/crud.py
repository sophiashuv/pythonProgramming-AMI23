from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc, cast, text
from sqlalchemy.inspection import inspect
import os
import json

from Product import Product


with open('secret.json') as f:
    SECRET = json.load(f)

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}".format(
    user=SECRET["user"],
    password=SECRET["password"],
    host=SECRET["host"],
    port=SECRET["port"],
    db=SECRET["db"])

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(Product, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(100), unique=False)
    _price = db.Column(db.Float(), unique=False)
    _image_url = db.Column(db.String(200), unique=False)
    _created_at = db.Column(db.String(20), unique=False)
    _updated_at = db.Column(db.String(20), unique=False)
    description = db.Column(db.String(500), unique=False)

    def __init__(self, **d):
        super().__init__(**d)


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', '_title', '_price',
                  '_image_url', '_created_at', '_updated_at',
                  'description')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route("/posts", methods=["POST"])
def create():
    try:
        product = Product(title=request.json['title'], price=request.json['price'], image_url=request.json['image_url'],
                          created_at=request.json['created_at'], updated_at=request.json['updated_at'],
                          description=request.json['description'])
        db.session.add(product)
        db.session.commit()
        return product_schema.jsonify(product)
    except Exception as e:
        return abort(400, e)


@app.route("/posts", methods=["GET"])
def posts():
    sort_by = request.args.get('sort_by')
    sort_type = request.args.get('sort_type', default='desc')
    s = request.args.get('s')
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', type=int)
    products = Product.query
    len_products = len(products_schema.dump(products))

    if sort_by is not None:
        try:
            if sort_type == "asc":
                products = products.order_by(sort_by)

            else:
                products = products.order_by(desc(sort_by))
        except Exception as e:
            return abort(404, e)

    if s is not None:
        b = Product._title.like('%' + s + '%')
        for column in inspect(Product).c:
             b |= cast(getattr(Product, column.name), db.String).like('%' + s + '%')

        products = products.filter(b)

    if limit is not None:
        products = products.offset(offset * limit).limit(limit)

    products = products_schema.dump(products)
    return jsonify({'products': products},
                   {'count': len_products})


@app.route("/posts/<int:id>", methods=["GET"])
def posts_detail(id):
    product = Product.query.get(id)
    if not product:
        return abort(404, "Product not find.")
    return product_schema.jsonify(product)


@app.route("/posts/<int:id>", methods=["DELETE"])
def posts_delete(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


@app.route("/posts/<int:id>", methods=["PUT"])
def post_update(id):
    product = Product.query.get(id)
    if not product:
        return abort(404, "Product not find.")
    try:
        product.title = request.json['title']
        product.price = request.json['price']
        product.created_at = request.json['created_at']
        product.updated_at = request.json['updated_at']
        product.description = request.json['description']
        db.session.commit()
    except Exception as e:
        return abort(400, e)

    return product_schema.jsonify(product)


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True, host='127.0.0.1')
