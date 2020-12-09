from app import *
from routes import *
from moduls.product.Product import *
from moduls.product.ProductSchema import *
from moduls.user.User import *
from moduls.user.UserSchema import *


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True, host='127.0.0.1')
