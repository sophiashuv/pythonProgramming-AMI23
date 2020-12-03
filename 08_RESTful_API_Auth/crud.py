from flask import Flask, jsonify, abort, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc, cast
from sqlalchemy.inspection import inspect
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (JWTManager, verify_jwt_in_request, create_access_token,get_jwt_claims)
import hashlib
import os
import json

from Product import Product
from User import User


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
app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'

app.config['JWT_SECRET_KEY'] = 'Dude!WhyShouldYouEncryptIt'
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)


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

class User(User, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    _first_name = db.Column(db.String(1000))
    _last_name = db.Column(db.String(1000))

    def __init__(self, **d):
        super().__init__(**d)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(_email=email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                '_email': x._email,
                'password': x.password
            }
        return {'users': [to_json(user) for user in User.query.all()]}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': f'{num_rows_deleted} row(s) deleted'}
        except:
            return {'message': 'Something went wrong'}


    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', '_email', 'password',
                  '_first_name', '_last_name')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/api/users', methods=['POST'])
def register():
    try:
        form = request.json
        if request.method == 'POST':
            hashed_password = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
            new_user = User(
                last_name=form["last_name"],
                first_name=form["first_name"],
                email=form["email"],
                password=hashed_password)

            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered', 'success')
            return user_schema.jsonify(new_user)
        else:
            abort(400)
    except Exception as e:
        return abort(400, e)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {"id": identity}


@app.route('/login', methods=['POST'])
def login():
    try:
        form = request.json
        hashed_password = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
        email = form["email"]
        user = User.find_by_email(email)
        if user.password == hashed_password:
            access_token = create_access_token(user.id)
            return jsonify(access_token=access_token)
        else:
            return abort(400, "Wrong password")
    except Exception as e:
        return abort(400, e)


@app.route("/posts", methods=["POST"])
def create():
    try:
        verify_jwt_in_request()
        claims = get_jwt_claims()
        product = Product(title=request.json['title'], price=request.json['price'], image_url=request.json['image_url'],
                          created_at=request.json['created_at'], updated_at=request.json['updated_at'],
                          description=request.json['description'], user_id = claims["id"])
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
    verify_jwt_in_request()
    claims = get_jwt_claims()
    products = Product.query.filter(Product.user_id == claims['id'])

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
    verify_jwt_in_request()
    claims = get_jwt_claims()
    product = Product.query.get(id)
    if not product or product.user_id != claims["id"]:
        return abort(404, "Product not find.")
    return product_schema.jsonify(product)


@app.route("/posts/<int:id>", methods=["DELETE"])
def posts_delete(id):
    verify_jwt_in_request()
    claims = get_jwt_claims()
    product = Product.query.get_or_404(id)
    if product.user_id == claims["id"]:
        db.session.delete(product)
        db.session.commit()
        return product_schema.jsonify(product)


@app.route("/posts/<int:id>", methods=["PUT"])
def post_update(id):
    verify_jwt_in_request()
    claims = get_jwt_claims()
    product = Product.query.get(id)
    if not product or product.user_id != claims["id"]:
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
