from app import *
from routes import *

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True, host='127.0.0.1')

