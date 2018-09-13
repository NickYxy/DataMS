__author__ = 'nickyuan'


from app import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), unique=True, nullable=False)
    last_ = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, name=None, email=None, mobile=None):
        self.name = name
        self.email = email
        self.mobile = mobile

    def __repr__(self):
        return '<User %r>' % self.username
