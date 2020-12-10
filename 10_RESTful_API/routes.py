from flask import jsonify, abort
from sqlalchemy import desc, cast
from sqlalchemy.inspection import inspect
from flask_jwt_extended import verify_jwt_in_request, create_access_token, get_jwt_claims
from flask import flash, request
import hashlib
from datetime import date

from app import *
from routes import *
from moduls.product.Product import *
from moduls.product.ProductSchema import *
from moduls.user.User import *
from moduls.user.UserSchema import *
from moduls.order.Order import *
from moduls.order.OrderSchema import *
from Validation import *


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


@app.route('/api/users', methods=['POST'])
def register():
    form = request.json
    try:
        hashed_password = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
        new_user = User(
            last_name=form["last_name"],
            first_name=form["first_name"],
            email=form["email"],
            password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered', 'success')
        return user_schema.jsonify(new_user), 201

    except Exception as e:
        return jsonify(status="404", errors=str(e)), 400


""" TODO """
# def admin_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         verify_jwt_in_request()
#         claims = get_jwt_claims()
#         if claims['role'] != 'admin':
#             return jsonify(msg='Admins only!'), 403
#         else:
#             return fn(*args, **kwargs)
#     return wrapper
#
#
# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     if identity == 'admin':
#         return {'role': 'admin'}
#     else:
#          return {'role': 'user'}


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {"id": identity}


@app.route('/login', methods=['POST'])
def login():
    form = request.json
    hashed_password = hashlib.sha256(form['password'].encode('utf-8')).hexdigest()
    email = form["email"]
    user = User.find_by_email(email)
    if not user:
        return jsonify(status='404', message='Incorrect login.'), 404
    if user.password == hashed_password:
        access_token = create_access_token(user.id)
        return jsonify(access_token=access_token), 201
    else:
        return jsonify(status='404', message='Incorrect login or password.'), 404


@app.route("/posts", methods=["POST"])
def create():
    try:
        verify_jwt_in_request()
        claims = get_jwt_claims()
        user_admin = User.query.get(claims["id"])
        Validation.validateAdmin(user_admin.role)
        product = Product(title=request.json['title'], price=request.json['price'], image_url=request.json['image_url'],
                          created_at=request.json['created_at'], updated_at=request.json['updated_at'],
                          description=request.json['description'], user_id=claims["id"], amount=request.json['amount'])
        db.session.add(product)
        db.session.commit()
        return product_schema.jsonify(product), 201
    except Exception as e:
        return jsonify(status='400', message=str(e)), 400


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
                   {'count': len_products}), 201


@app.route("/posts/<int:id>", methods=["GET"])
def posts_detail(id):
    product = Product.query.get(id)
    if not product:
        return jsonify(status='404', message="Product not find."), 404
    return product_schema.jsonify(product), 201


@app.route("/posts/<int:id>", methods=["DELETE"])
def posts_delete(id):
    verify_jwt_in_request()
    claims = get_jwt_claims()
    user_admin = User.query.get(claims["id"])
    try:
        Validation.validateAdmin(user_admin.role)
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return product_schema.jsonify(product), 201
    except Exception as e:
        return jsonify(status='404', message=str(e)), 404


@app.route("/posts/<int:id>", methods=["PUT"])
def post_update(id):
    verify_jwt_in_request()
    claims = get_jwt_claims()
    user_admin = User.query.get(claims["id"])
    try:
        Validation.validateAdmin(user_admin.role)
        product = Product.query.get_or_404(id)
        product.title = request.json['title']
        product.price = request.json['price']
        product.created_at = request.json['created_at']
        product.updated_at = request.json['updated_at']
        product.description = request.json['description']
        product.user_id = claims["id"]
        product.amount = request.json['amount']
        db.session.commit()
        return product_schema.jsonify(product), 201
    except Exception as e:
        return jsonify(status='404', message=str(e)), 404


@app.route('/api/orders', methods=['POST'])
def create_order():
    verify_jwt_in_request()
    claims = get_jwt_claims()
    try:
        order = Order(user_id=claims["id"],
                      product_id=request.json["product_id"],
                      amount=request.json["amount"],
                      date=str(date.today()))
        product = Product.query.get_or_404(request.json["product_id"])
        product.amount = product.amount - request.json["amount"]
        db.session.add(order)
        db.session.commit()
        return order_schema.jsonify(order), 201
    except Exception as e:
        return jsonify(status='404', message=str(e)), 404


@app.route('/api/orders', methods=['GET'])
def orders():
    try:
        verify_jwt_in_request()
        claims = get_jwt_claims()
        orders = Order.query.filter(Order.user_id == claims['id'])
        len_orders = len(products_schema.dump(orders))
        orders = products_schema.dump(orders)
        return jsonify({'products': orders},
                       {'count': len_orders}), 201
    except Exception as e:
        return jsonify(status='404', message=str(e)), 404


@app.route('/api/orders/<id>', methods=['GET'])
def order_detail(id):
    try:
        verify_jwt_in_request()
        claims = get_jwt_claims()
        order = Order.query.get_or_404(id)
        if order.user_id == claims['id']:
            return product_schema.jsonify(order), 201
        else:
            return jsonify(status='404', message="Id doesnt exist"), 404
    except Exception as e:
        return jsonify(status='404', message=str(e)), 404
