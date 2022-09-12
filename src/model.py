from . import db
from datetime import datetime
from flask_login import UserMixin

class Articles(db.Model):
    __tablename__ = "articles"

    key = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    type = db.Column(db.Text)
    description = db.Column(db.Text)
    author = db.Column(db.Text)
    directory = db.Column(db.Text)
    views = db.Column(db.Integer, default=0)
    uploaded = db.Column(db.Text, default=datetime.now().strftime('%m-%d-%Y'))

class Users(db.Model, UserMixin):
    __tablename__ = "users"

    key = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def get_id(self):
        return (self.key)

class Comments(db.Model):
    __tablename__ = "comments"

    key = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Text)
    article = db.Column(db.Text) #connects to article directory
    parent = db.Column(db.Text, default="") #connects to comment key
    content = db.Column(db.Text)
    date_commented = db.Column(db.Text, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

class Upvotes(db.Model):
    __tablename__ = "upvotes"

    key = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text) #connects to comment key
    user = db.Column(db.Text) #connects to user key

class Downvotes(db.Model):
    __tablename__ = "downvotes"

    key = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text) #connects to comment key
    user = db.Column(db.Text) #connects to user key