from datetime import datetime as dt

class Post:
    _list = []

    def __init__(self, _id, image, email, title, body):
        self._id = _id
        self.email = email
        self.image = image
        self.title = title
        self.body = body
        self.created_on = dt.utcnow()
        self._list.append(self)

    # def from_dict(self):
    #     pass

    def to_dict(self):
        return {
            'id': self._id,
            'email': self.email,
            'image': self.image,
            'title': self.title,
            'body': self.body,
            'created_on': dt.strftime(self.created_on, '%m/%d/%Y')
        }

    def __repr__(self):
        return f'<Post: [{self.email}]: {self.body[:20]}...>'