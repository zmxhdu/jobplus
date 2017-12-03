# coding = utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Base(db.Model):
    """ 所有model的一个基类，默认添加了时间戳"""
    __abstract__ = True
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


user_job = db.Table(
    'user_job',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
)


class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    collect_jobs = db.relationship('Job', secondary=user_job)
    job_experiences = db.Column(db.String(1024))
    edu_experiences = db.Column(db.String(1024))
    project_experiences = db.Column(db.String(1024))

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    salary_low = db.Column(db.Integer, nullable=False)
    salary_high = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(24))
    tags = db.Column(db.String(128))
    job_requirement = db.Column(db.String(1024))
    copmany_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    copmany = db.relationship('Company', uselist=False)

    def __repr__(self):
        return '<Job:{}>'.format(self.name)


class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(24), nullable=False)
    location = db.Column(db.String(24), nullable=False)
    # 公司描述
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('company', uselist=False))

    def __repr__(self):
        return '<Company:{}>'.format(self.name)


class Status(Base):
    __tablename__ = 'status'

    # 等待企业审核
    STATUS_WAITING = 1
    # 被拒绝
    STATUS_REJECT = 2
    # 被接收，等待通知面试
    STATUS_ACCEPT = 3

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
    status = db.Column(db.SmallInteger, default=STATUS_WAITING)
