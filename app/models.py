from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    domains = db.relationship('Domain', backref='user', lazy='dynamic')


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
