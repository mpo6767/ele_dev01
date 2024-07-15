from election1.extensions import (db, login_manager)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from election1.utils import unique_security_token

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class Classgrp(db.Model):
    id_classgrp = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=45), nullable=False,unique=True)
    sortkey = db.Column(db.Integer, nullable=False, unique=True)
    candidates = db.relationship('Candidate',  cascade="all, delete-orphan",backref='classgrp')


class Office(db.Model):
    id_office = db.Column(db.Integer, primary_key=True)
    office_title = db.Column(db.String(length=45), nullable=False, unique=True)
    office_vote_for = db.Column(db.Integer, default=1)
    sortkey = db.Column(db.Integer, nullable=False, unique=True)
    candidates = db.relationship('Candidate', cascade="all, delete-orphan", backref='office')


class Candidate(db.Model):
    id_candidate = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(length=45), nullable=False)
    lastname = db.Column(db.String(length=45), nullable=False)
    id_classgrp = db.Column(db.Integer, db.ForeignKey('classgrp.id_classgrp'), nullable=False)
    id_office = db.Column(db.Integer, db.ForeignKey('office.id_office'), nullable=False)
    votes = db.relationship('Votes', backref='candidate')


class User(db.Model, UserMixin):
    id_user = db.Column(db.Integer, primary_key=True)
    user_firstname = db.Column(db.String(length=45), nullable=False)
    user_lastname = db.Column(db.String(length=45), nullable=False)
    user_so_name = db.Column(db.String(length=30), nullable=False, unique=True)
    user_pass = db.Column(db.String(256))

    user_email = db.Column(db.String(45), unique=True)
    user_status = db.Column(db.Integer, default=False, nullable=False)
    user_pw_change = db.Column(db.String(length=1))
    user_security = db.Column(db.String(138), default=unique_security_token)
    user_created = db.Column(db.DateTime, default=datetime.now)
    user_sec_send = db.Column(db.DateTime, default=datetime.now)

    id_admin_role = db.Column(db.Integer, db.ForeignKey('admin_roles.id_admin_role'))

    def get_id(self):
        return (self.id_user)





class Admin_roles(db.Model):
    id_admin_role = db.Column(db.Integer, primary_key=True)
    admin_role_name = db.Column(db.String(length=45), nullable=False, unique=True)
    user = db.relationship('User', backref='admin_roles')


class Dates(db.Model):
    iddates = db.Column(db.Integer, primary_key=True)
    # had to change because of SQLite does not have a datetime column
    # start_date_time = db.Column(db.DateTime, nullable=False)
    # end_date_time = db.Column(db.DateTime, nullable=False)

    # sQLite stored as epoch integer
    start_date_time = db.Column(db.Integer, nullable=False)
    end_date_time = db.Column(db.Integer, nullable=False)




class Votes(db.Model):
    id_votes = db.Column(db.Integer, primary_key=True)
    votes_token = db.Column(db.String(138), nullable=False)
    id_candidate = db.Column(db.Integer, db.ForeignKey('candidate.id_candidate'))



class Tokenlist(db.Model):
    id_tokenlist = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(138), nullable=False)
    vote_submitted_date_time = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        """
        Convert the Tokenlist object into a dictionary format.
        """
        return {
            'id_tokenlist': self.id_tokenlist,
            'token': self.token,
            'vote_submitted_date_time': self.vote_submitted_date_time.isoformat() if self.vote_submitted_date_time else None
        }


