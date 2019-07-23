
from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
    )
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), default="")
    text = db.Column(db.Text, default="")

    def __init__(self, title, text):
        self.title = title
        self.text = text


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)