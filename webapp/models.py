from flask_login import UserMixin

from . import db


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return self.username
