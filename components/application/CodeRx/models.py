from CodeRx import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

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
'''
roles_probs = db.Table('roles_probs',
    db.Column('prob_id', db.Integer(), db.ForeignKey('prob_id')),
    db.Column('submitted_id', db.Integer(), db.ForeignKey('submitted_id'))

class Problem(db.Model, ProblemMixin):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))
    language = db.Column(db.String(225))
    testcase = db.Column(db.String(225))
    initial_file = db.Column(db.String(225))
    allowmultiplefiles = db.Column(db.String(225))
    created_date = db.Column(db.DateTime())
    due_date = db.Column(db.DateTime())

class Submitted(db.Model, SumbittedMixin):
    id = db.Column(db.Integer, primary_key=True)
    prob_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, unique=True)
    files = db.Column(db.String(225))
    new_field = db.Column(db.String(225))
    test_case_results = db.Column(db.String(255))

class files(db.Model, filesMixin):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(225))
    content = db.Column(db.String(225))

class testcase(db.Model, testcaseMixin):
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.String(225))
    expected_output = db.Column(db.String(225))
    hidden = db.Column(db.String(225))

class test_case_results(db.Model, test_case_resultsMixin):
    id = db.Column(db.Integer, primary_key=True)
    testcase_id = db.Column(db.String(225))
    passs = db.Column(db.String(225))
'''
