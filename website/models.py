from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    week = db.Column(db.Integer) # 1, 2, or 3
    winners = db.Column(MutableList.as_mutable(PickleType), default=[]) # List of all winners picked
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Matchup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    week = db.Column(db.Integer) # 1, 2, or 3
    bracket = db.Column(db.String(5)) # North, South, West, or East
    team1 = db.Column(db.String(100)) # Name of Team 1
    team2 = db.Column(db.String(100)) # Name of Team 2

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    picks = db.relationship('Picks')

class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pool_name = db.Column(db.String(100))
    password = db.Column(db.String(12))

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pool_id = db.Column(db.Integer, db.ForeignKey('pool.id'))
    
