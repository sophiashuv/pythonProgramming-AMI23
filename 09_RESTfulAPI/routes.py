from sqlalchemy import desc, cast
from sqlalchemy.inspection import inspect
from flask import request, jsonify, abort
from app import *
from moduls.product.Product import *
from moduls.product.ProductSchema import *


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