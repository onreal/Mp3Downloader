from datetime import datetime
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    modifieddatetime = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.hash_password(password)
        self.modifieddatetime = datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'email': self.email,
            'password': self.password
        }

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
