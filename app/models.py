from datetime import datetime
from app import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    feedback = db.Column(db.Text)
    created = db.Column(db.DateTime)
