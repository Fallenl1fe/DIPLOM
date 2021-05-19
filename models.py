from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app=app)



class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    devision_id = db.Column(db.Integer)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    role = db.Column(db.Boolean, default=0)
    teststatus = db.Column(db.Boolean, default=0)
    tested = db.Column(db.Boolean, default=0)
    rating = db.Column(db.Float, default=0)

    pr = db.relationship('Posts', backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.id}>"

class Posts(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    text = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"
