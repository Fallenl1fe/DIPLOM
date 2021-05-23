import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref

from app import app

db = SQLAlchemy(app=app)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    devision_id = db.Column(db.Integer, db.ForeignKey('devisions.id'))
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    role = db.Column(db.Boolean, default=0)
    rating = db.Column(db.Float, default=0)

    #post_rl = db.relationship('Posts', backref='users_posts')
    #chat_rl = db.relationship('Chats', backref='users_chats')

    def __repr__(self):
        return f"<users {self.id}>"


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',  ondelete="CASCADE", onupdate="CASCADE"))

    #ForeignKey('parent.id', ondelete="CASCADE", ondelete="CASCADE")

    def __repr__(self):
        return f"<posts {self.id}>"


class Devisions(db.Model):
    __tablename__ = 'devisions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)

    #devis_rl = db.relationship('devisions', backref='devis_users')

    def __repr__(self):
        return f"<devisions {self.id}>"


class Chats(db.Model):
    __tablename__ = 'chats'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    telegram_user_id = db.Column(db.Integer, primary_key=True)


class Temas(db.Model):
    __tablename__ = 'temas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)


class Tests(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_create = db.Column(db.DateTime)
    max_test_time = db.Column(db.Integer)
    max_q = db.Column(db.Integer)
    tema_id = db.Column(db.Integer, db.ForeignKey('temas.id'))

    tema = relationship("Temas")

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    q_text = db.Column(db.Text)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    a_text = db.Column(db.String(100))
    correct_a = db.Column(db.Boolean)


class Protocols(db.Model):
    __tablename__ = 'protocols'

    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), primary_key=True)
    testing_id = db.Column(db.Integer, db.ForeignKey('answers.id'), primary_key=True)


# Добавить поля связей
# по типу devis_rl = db.relationship('devisions', backref='devis_users')


class Testing(db.Model):
    __tablename__ = 'testing'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    result = db.Column(db.Boolean, nullable=True)
    a_number = db.Column(db.Integer, nullable=True)


class User_test(db.Model):
    __tablename__ = 'user_test'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), primary_key=True)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    max_try = db.Column(db.Integer, default=3)
    trying = db.Column(db.Integer, default=0)


db.create_all()