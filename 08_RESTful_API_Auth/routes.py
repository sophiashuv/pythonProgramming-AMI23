from flask import jsonify, abort, request
from sqlalchemy import desc, cast
from sqlalchemy.inspection import inspect
from flask_jwt_extended import verify_jwt_in_request, create_access_token,get_jwt_claims
import hashlib

from app import *
from routes import *
from moduls.product.Product import *
from moduls.product.ProductSchema import *
from moduls.user.User import *
from moduls.user.UserSchema import *


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
    if not product or product.user_id != claims["id"]:
        return abort(404, "Product not find.")
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

