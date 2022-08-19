from . import db
from datetime import datetime

class Articles(db.Model):
    __tablename__ = "articles"

    key = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    type = db.Column(db.Text)
    description = db.Column(db.Text)
    author = db.Column(db.Text)
    directory = db.Column(db.Text)
    views = db.Column(db.Integer, default=0)
    uploaded = db.Column(db.Text, default=datetime.now().strftime('%m-%d-%Y %H:%M:%S'))