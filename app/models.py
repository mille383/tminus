from datetime import datetime as dt
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    body = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    # def from_dict(self):
    #     pass

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'image': self.image,
            'title': self.title,
            'body': self.body,
            'created_on': dt.strftime(self.created_on, '%m/%d/%Y')
        }

    def __repr__(self):
        return f'<Post: [{self.email}]: {self.body[:20]}...>'