from passlib.hash import pbkdf2_sha256 as sha256

from moduls.user.User import User
from app import *


class User(User, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    _first_name = db.Column(db.String(1000))
    _last_name = db.Column(db.String(1000))
    role = db.Column(db.String(5))

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
                'username': x.username,
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
