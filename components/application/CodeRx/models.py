from CodeRx import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return str(self.name)


problem_users = db.Table('problem_users',
                         db.Column('user_id', db.Integer,
                                   db.ForeignKey('user.id')),
                         db.Column('problem_id', db.Integer, db.ForeignKey('problem.id')))

class_users = db.Table('class_users',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('class_id', db.Integer, db.ForeignKey('class.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    name = db.Column(db.String)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    submissions = db.relationship("Submission")
    assigned_problems = db.relationship('Problem', secondary=problem_users)
    last_problem_id = db.Column(db.Integer)
    classes = db.relationship('Class', secondary=class_users,
                              backref=db.backref('users', lazy='dynamic'))


class_problem = db.Table('class_problem',
                         db.Column('problem_id', db.Integer,
                                   db.ForeignKey('problem.id')),
                         db.Column('class_id', db.Integer, db.ForeignKey('class.id')))


class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    problems = db.relationship('Problem', secondary=class_problem,
                               backref=db.backref('class', lazy='dynamic'))
    professor_id = db.Column(db.Integer)
    join_code = db.Column(db.String, unique=True)


class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    language = db.Column(db.String)
    allowmultiplefiles = db.Column(db.Boolean)
    entry_command = db.Column(db.String)
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    submissions = db.relationship("Submission")
    test_cases = db.relationship("TestCase")
    files = db.relationship("Problem_Base_File")


class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    files = db.Column(db.String)
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    test_case_results = db.relationship("Test_case_results")
    files = db.relationship("Submission_File")
    final_submission = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    submission_time = db.Column(db.DateTime)
    grade = db.Column(db.Integer)
    # Comments


class Problem_Base_File(db.Model):
    __tablename__ = 'problembasefile'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    content = db.Column(db.String)
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))


class Submission_File(db.Model):
    __tablename__ = "submission_file"
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    content = db.Column(db.String)
    submission_id = db.Column(db.Integer, db.ForeignKey("submission.id"))


class TestCase(db.Model):
    __tablename__ = 'testcase'
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.String)
    expected_output = db.Column(db.String)
    hidden = db.Column(db.Boolean)
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))


class Test_case_results(db.Model):
    __tablename__ = 'test_case_results'
    id = db.Column(db.Integer, primary_key=True)
    pass_state = db.Column(db.Boolean)
    testcase_id = db.Column(db.Integer, db.ForeignKey("submission.id"))
