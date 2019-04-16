from CodeRx import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
        db.Column('prob_id', db.Integer(), db.ForeignKey('prob_id')),
        db.Column('submitted_id', db.Integer(), db.ForeignKey('submitted_id'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
                       
class Problem(db.Model, ProblemMixin):
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.Integer, unique=True)
    description = db.Column(db.String(255))
                       
class Submitted(db.Model, SumbittedMixin):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    description = db.Column(db.String(255))
