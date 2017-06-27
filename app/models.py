# -*- coding: UTF-8 -*-

from datetime import datetime
from random import randint
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from . import db
from . import login_manager


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    depname = db.Column(db.String(250))
    users = db.relationship('User', backref='dep', lazy='dynamic')

    @staticmethod
    def generate_fake(count=20):
        """Generate fake departments data."""
        from sqlalchemy.exc import IntegrityError
        from faker import Factory
        fake = Factory.create('ru_RU')
        for k in range(count):
            db.session.add(Department(depname=fake.job()))
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


class Comment(db.Model):
    """Comments for gems. One gem can contain many comments."""
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    comment = db.Column(db.String(500))
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    gem_id = db.Column(db.Integer, db.ForeignKey('gems.id'))


class Team(db.Model):
    """Team of Users that can participate in Gem."""
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    gem_id = db.Column(db.Integer, db.ForeignKey('gems.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    last_login = db.Column(db.DateTime)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    active = db.Column(db.Integer, default=1)  # 0 = blocked, 1 = active
    dep_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role = db.Column(db.Integer, default=0)  # 0-User, 1-Moderator, 2-Admin
    # Relationships
    comments = db.relationship('Comment', backref='comment_author', lazy='dynamic')
    drafts = db.relationship('Draft', backref='draft_author', lazy='dynamic')
    proposals = db.relationship('Proposal', backref='proposal_author', lazy='dynamic')
    trashes = db.relationship('Trash', backref='trash_author', lazy='dynamic')
    gems = db.relationship('Gem', backref='gem_author', lazy='dynamic')
    teams = db.relationship('Team', backref='team_member', lazy='dynamic')

    def verify_password(self, password):
        return self.password == password
    
    def is_active(self):
        """Return True if User is active user. False otherwise."""
        return self.active == 1
    
    @staticmethod
    def generate_fake(count=100):
        """Generate fake users."""
        from sqlalchemy.exc import IntegrityError
        from faker import Factory
        fake = Factory.create('ru_RU')
        for k in range(count):
            _usr = User(
                created=datetime.utcnow(),
                username=fake.name(),
                email=fake.email(),
                password="qwerty",
                dep_id=randint(1, 15),
                role=0
            )
            if k in range(0, 10, 10):
                _usr.role = 1  # moderator
            if k in (10, 20):
                _usr.role = 2  # admin
            db.session.add(_usr)
        try:
            db.session.commit()
        except IntegrityError as int_error:
            db.session.rollback()


class Document(object):
    """Abstract Base Class for documents."""
    @declared_attr
    def id(cls):
        return db.Column(db.Integer, primary_key=True)

    @declared_attr
    def created(cls):
        return db.Column(db.DateTime, default=datetime.utcnow())
    
    @declared_attr
    def name(cls):
        return db.Column(db.String(300))

    @declared_attr
    def cause(cls):
        return db.Column(db.String(1000))
    
    @declared_attr
    def description(cls):
        return db.Column(db.String(3000))

    @declared_attr
    def plan(cls):
        return db.Column(db.String(3000))
    
    @declared_attr
    def number(cls):
        return db.Column(db.Integer, default=0)


class Draft(Document, db.Model):
    __tablename__ = 'drafts'
    author = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def _generate_number():
        return randint(100000, 999999)

    @staticmethod
    def generate_fake(count=100):
        """Generate fake drafts."""
        from sqlalchemy.exc import IntegrityError
        from faker import Factory
        fake = Factory.create('ru_RU')
        for k in range(count):
            fake_draft = Draft(
                created=datetime.utcnow(),
                author=randint(0, 99),
                name=fake.text(max_nb_chars=299),
                cause=fake.text(max_nb_chars=999),
                description=fake.text(max_nb_chars=2999),
                number=randint(100000,999999),
                plan=fake.text(max_nb_chars=2999)
            )
            db.session.add(fake_draft)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


class Proposal(Document, db.Model):
    __tablename__ = 'proposals'
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    @staticmethod
    def generate_fake(count=50):
        """Generate fake proposals."""
        from sqlalchemy.exc import IntegrityError
        from faker import Factory
        fake = Factory.create('ru_RU')
        for k in range(count):
            fake_proposal = Proposal(
                created=datetime.utcnow(),
                author=randint(0, 99),
                name=fake.text(max_nb_chars=299),
                cause=fake.text(max_nb_chars=999),
                description=fake.text(max_nb_chars=2999),
                number=randint(1000,9999),
                plan=fake.text(max_nb_chars=2999)
            )
            db.session.add(fake_proposal)
        try:
            db.session.commit()
        except IntegrityError as int_error:
            db.session.rollback()


class Trash(Document, db.Model):
    __tablename__ = 'trashes'
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    trash_reason = db.Column(db.String(1000))


class Gem(Document, db.Model):
    __tablename__ = 'gems'
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    closed_at = db.Column(db.DateTime)
    # Relationship
    comments = db.relationship('Comment', backref='comment_gem', lazy='dynamic')
    teams = db.relationship('Team', backref='tean_gem', lazy='dynamic')
    
    @staticmethod
    def generate_fake(count=50):
        """Generate fake gems."""
        import random
        from sqlalchemy.exc import IntegrityError
        from faker import Factory
        fake = Factory.create('ru_RU')
        for k in range(count):
            fake_gem = Gem(
                created=datetime.utcnow(),
                author=randint(0, 99),
                name=fake.text(max_nb_chars=299),
                cause=fake.text(max_nb_chars=999),
                description=fake.text(max_nb_chars=2999),
                number=randint(1000, 9999),
                plan=fake.text(max_nb_chars=2999)
            )
            db.session.add(fake_gem)
        try:
            db.session.commit()
        except IntegrityError as int_error:
            db.session.rollback()

# ---------------------------------------------------------------------------- #
# ----- Utilities ------------------------------------------------------------ #
# ---------------------------------------------------------------------------- #

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
